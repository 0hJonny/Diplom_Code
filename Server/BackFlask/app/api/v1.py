import base64
import psycopg2
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.database import articles_connection
from models import ArticleParser, ArticleAnnotation
from utils import MinioClientFactory

api_v1_bp = Blueprint('api_v1', __name__)

# Search functions
def get_language_id(language_code, cursor):
    cursor.execute("SELECT language_id FROM languages WHERE language_code = %s", (language_code,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        raise ValueError(f"Language with code '{language_code}' not found in the database")


@api_v1_bp.route('/articles/check', methods=['GET'])
@jwt_required()
def article_check():
    current_user = get_jwt_identity()

    if request.method == 'GET':

        if not request.is_json:
            return "Unsupported Media Type: Expecting JSON", 415

        article_href = request.get_json().get('article_href')

        if not article_href:
            return jsonify({"error": "Missing 'href' parameter"}), 400
        try:
            with psycopg2.connect(articles_connection) as connection:
                with connection.cursor() as cursor:
                    # SQL-запрос для выбора статьи по ее ссылке
                    query = "SELECT EXISTS(SELECT 1 FROM articles WHERE source_link = %s)"
                    cursor.execute(query, (article_href,))
                    article_exists = cursor.fetchone()[0]

            return jsonify({"article_exists": article_exists}), 200
        except psycopg2.Error as err:
            return f"Error checking article existence: {err}", 500

@api_v1_bp.route('/articles/count', methods=['GET'])
def articles_count():
    if request.method == 'GET':
        category = request.args.get('category', default='')

        query_count = """
            SELECT 
                COUNT(articles.id)
            FROM 
                articles
            LEFT JOIN 
                themes ON articles.theme_id = themes.theme_id
            LEFT JOIN 
                annotations ON articles.id = annotations.article_id
        """

        if category:
            query_count += " WHERE themes.theme_name = %s AND annotations.article_id IS NOT NULL"
        else:
            query_count += " WHERE annotations.article_id IS NOT NULL"
        query_count += ";"

        with psycopg2.connect(articles_connection) as connection:
            with connection.cursor() as cursor:
                try:
                    if category:
                        cursor.execute(query_count, (category,))
                    else:
                        cursor.execute(query_count)
                    count = cursor.fetchone()[0]
                    result = {"count": count}
                    return jsonify(result)
                except psycopg2.Error as err:
                    return f"Database error: {err}", 500

@api_v1_bp.route('/articles', methods=['GET', 'POST'])
# @jwt_required()
def protected_articles():
    # current_user = get_jwt_identity()

    if request.method == 'GET':
        # if not request.is_json:
        #     return "Unsupported Media Type: Expecting JSON", 415
        category = request.args.get('category', default='')
        limit = request.args.get('limit', default=15, type=int)
        page = request.args.get('page', default=1, type=int)
        language_code = request.args.get('language_code', default='en')  # Получаем языковой код из запроса

        # Вычисляем смещение на основе номера страницы
        offset = (page - 1) * limit

        # TODO Проверка на раодной язык, если у статьи articles.language_id не равен языкам из других таблиц, значи язык - не родной


        query = """
            SELECT 
                articles.id, 
                COALESCE(titles.title, '') AS title, 
                articles.created_at, 
                articles.image_link, 
                themes.theme_name,
                json_agg(tags.tag_name) AS tags,
                annotations.annotation
            FROM 
                articles
            LEFT JOIN 
                themes ON articles.theme_id = themes.theme_id
            LEFT JOIN 
                article_tags ON articles.id = article_tags.article_id
            LEFT JOIN 
                tags ON article_tags.tag_id = tags.tag_id
            LEFT JOIN 
                annotations ON articles.id = annotations.article_id
            LEFT JOIN
                titles ON articles.id = titles.article_id AND titles.language_id = (
                    SELECT language_id FROM languages WHERE language_code = %s
                )
        """

        if category:
            query += " WHERE themes.theme_name = %s AND annotations.article_id IS NOT NULL"
        else:
            query += " WHERE annotations.article_id IS NOT NULL"

        query += " GROUP BY articles.id, titles.title, themes.theme_name, annotations.annotation"
        query += " ORDER BY articles.created_at DESC"
        query += " LIMIT %s OFFSET %s;"

        with psycopg2.connect(articles_connection) as connection:
            with connection.cursor() as cursor:
                try:
                    if category:
                        cursor.execute(query, (language_code, category, limit, offset))
                    else:
                        cursor.execute(query, (language_code, limit, offset))
                    articles = cursor.fetchall()
                    return jsonify(articles)
                except psycopg2.Error as err:
                    return f"Database error: {err}", 500

    if request.method == 'POST':
        if request.is_json:
            requested_data = request.get_json()
            language_code = requested_data["language_code"]
            data = ArticleParser(
                title=requested_data['title'],
                author=requested_data["author"],
                post_href=requested_data["post_href"],
                body=requested_data["body"],
                image = base64.b64decode(requested_data["image"])
            )
            with psycopg2.connect(articles_connection) as connection:
                with connection.cursor() as cursor:
                    try:

                        # Получение идентификатора языка
                        language_id = get_language_id(language_code, cursor)

                        # Вставка статьи в таблицу articles
                        # Подготовка SQL-запроса с использованием параметров
                        query = "INSERT INTO articles (author, source_link, body, language_id) VALUES (%s, %s, %s, %s) RETURNING id"
                        data_values = (data.author, data.post_href, data.body, language_id)

                        # Выполнение запроса с использованием параметров
                        cursor.execute(query, data_values)

                        # Получение значения id добавленной статьи
                        article_id = cursor.fetchone()[0]

                        # Вставка заголовка статьи в таблицу titles
                        query = "INSERT INTO titles (article_id, title, language_id) VALUES (%s, %s, %s)"
                        data_values = (article_id, data.title, language_id)

                        # Выполнение запроса с использованием параметров
                        cursor.execute(query, data_values)

                        # Загрузка изображения
                        minioFactory = MinioClientFactory()
                        minioClient = minioFactory.create_client()
                        minioClient.upload_image_from_bytes('images', f'{article_id}.png', data.image)
                        minioFactory.delete_clients()

                        connection.commit()
                    except psycopg2.Error as err:
                        connection.rollback()
                        return f"Article already exists! {err}", 500
                return {
                        "id": article_id,
                        "message": f"Article title:{data.title}, author:{data.author}, article href:{data.post_href}, article body:{data.body}, image is uploaded"
                    }, 201
        else:
            return "Unsupported Media Type: Expecting JSON", 415


@api_v1_bp.route('/articles/annotations', methods=['GET', 'POST'])
@jwt_required()
def annotations_api_last_needed():
    current_user = get_jwt_identity()
    
    if request.method == 'GET':
        query = """
            SELECT articles.id
            FROM articles
            LEFT JOIN annotations ON articles.id = annotations.article_id
            WHERE annotations.article_id IS NULL;
        """

        with psycopg2.connect(articles_connection) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                    annotations = cursor.fetchall()
                except psycopg2.Error as err:
                    return f"Database error: {err}", 500
        if annotations:
            return jsonify(annotations), 200
        else:
            return jsonify({'error': 'Annotations not found'}), 404

    if request.method == 'POST':
        pass

@api_v1_bp.route('/articles/annotations/<uuid:article_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def article_annotations_api_by_id(article_id):
    current_user = get_jwt_identity()

    if request.method == 'GET':
        article_id = str(article_id)

        query = """

        SELECT 
            articles.id AS id,
            titles.title AS title,
            articles.body AS body,
            languages.language_code AS language_code
        FROM 
            articles
        JOIN 
            titles ON articles.id = titles.article_id
        JOIN 
            languages ON titles.language_id = languages.language_id
        WHERE 
            articles.id = %s;
        """

        with psycopg2.connect(articles_connection) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, (article_id,))
                    article = cursor.fetchone()
                except psycopg2.Error as err:
                    return f"Database error: {err}", 500
        if article:
            return jsonify(article), 200
        else:
            return jsonify({'error': 'Article not found'}), 404

    if request.method == 'POST':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass

@api_v1_bp.route('/articles/<uuid:article_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def article_api_by_id(article_id):
    current_user = get_jwt_identity()

    if request.method == 'GET':
        article_id = str(article_id)

        query = """
            SELECT 
                articles.id, 
                titles.title, 
                articles.created_at,
                articles.source_link,  
                articles.body, 
                themes.theme_name,
                json_agg(tags.tag_name) AS tags,
                annotations.annotation,
                languages.language_code
            FROM 
                articles
            LEFT JOIN 
                themes ON articles.theme_id = themes.theme_id
            LEFT JOIN 
                article_tags ON articles.id = article_tags.article_id
            LEFT JOIN 
                tags ON article_tags.tag_id = tags.tag_id
            LEFT JOIN 
                annotations ON articles.id = annotations.article_id
            LEFT JOIN
                titles ON articles.id = titles.article_id
            LEFT JOIN
                languages ON titles.language_id = languages.language_id
            WHERE 
                articles.id = %s
            GROUP BY 
                articles.id, titles.title, themes.theme_name, annotations.annotation, languages.language_code;
        """

        with psycopg2.connect(articles_connection) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query, (article_id,))
                    article = cursor.fetchone()
                except psycopg2.Error as err:
                    return f"Database error: {err}", 500
        if article:
            return jsonify(article), 200
        else:
            return jsonify({'error': 'Article not found'}), 404

    if request.method == 'POST':
        article_id = str(article_id)

        if request.is_json:
            requested_data = request.get_json()
            data = ArticleAnnotation.get_json(requested_data)

            # Check if the article ID in the request body matches the article ID in the URL
            if data.id != article_id:
                return jsonify({'error': 'Article ID in the request body does not match the article ID in the URL'}), 400

            query_annotation = """
                INSERT INTO annotations (article_id, annotation, language_code, neural_network)
                VALUES (%s, %s, %s, %s)
            """
            with psycopg2.connect(articles_connection) as connection:
                with connection.cursor() as cursor:
                    try:
                        # Получение language_id для указанного языка
                        language_id = get_language_id(data.language_code, cursor)

                         # Запрос language_id из таблицы articles для указанного article_id
                        query_article_language_id = "SELECT language_id FROM articles WHERE id = %s"
                        cursor.execute(query_article_language_id, (data.id,))
                        article_language_id = cursor.fetchone()[0]

                        # Проверка, отличаются ли language_id
                        if article_language_id != language_id:
                            # Вставка заголовка в таблицу titles
                            query_title = """
                                INSERT INTO titles (article_id, title, language_id, neural_network)
                                VALUES (%s, %s, %s, %s)
                            """
                            cursor.execute(query_title, (data.id, data.title, language_id, data.neural_networks["translator"]))

                        # Вставка аннотации
                        cursor.execute(query_annotation, (data.id, data.annotation, language_id, data.neural_networks["annotator"]))

                        # Вставка темы, если она не существует, и получение ее theme_id
                        theme_id = insert_theme(data.theme_name, cursor)

                        # Обновление связи статьи с темой
                        update_article_theme(data.id, theme_id, cursor)

                        # Вставка тегов, если они не существуют, и получение их tag_ids
                        tag_ids = insert_tags(data.tags, cursor)

                        # Вставка связей статьи с тегами в таблицу article_tags
                        insert_article_tags(data.id, tag_ids, cursor)

                        connection.commit()
                        return jsonify({'message': f'Annotation created successfully for article {data.id}!'}), 201

                    except psycopg2.Error as err:
                        connection.rollback()
                        return f"Database error: {err}", 500

def insert_theme(theme_name, cursor):
                            cursor.execute("SELECT theme_id FROM themes WHERE theme_name = %s", (theme_name,))
                            existing_theme = cursor.fetchone()
                            if existing_theme:
                                return existing_theme[0]
                            else:
                                cursor.execute("INSERT INTO themes (theme_name) VALUES (%s) RETURNING theme_id", (theme_name,))
                                new_theme_id = cursor.fetchone()[0]
                                return new_theme_id
                
def update_article_theme(article_id, theme_id, cursor):
    cursor.execute("UPDATE articles SET theme_id = %s WHERE id = %s", (theme_id, article_id))

def insert_tags(tags, cursor):
    tag_ids = []
    for tag in tags:
        cursor.execute("SELECT tag_id FROM tags WHERE tag_name = %s", (tag,))
        existing_tag = cursor.fetchone()
        if existing_tag:
            tag_ids.append(existing_tag[0])
        else:
            cursor.execute("INSERT INTO tags (tag_name) VALUES (%s) RETURNING tag_id", (tag,))
            new_tag_id = cursor.fetchone()[0]
            tag_ids.append(new_tag_id)
    return tag_ids

def insert_article_tags(article_id, tag_ids, cursor):
    for tag_id in tag_ids:
        cursor.execute("INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)", (article_id, tag_id))


    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass