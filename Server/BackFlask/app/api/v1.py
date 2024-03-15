import psycopg2
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from PostgreSQL import DB_INSERT_TABLE_ARTICLES
from utils.database import articles_connection
from models import Article, Annotation

api_v1_bp = Blueprint('api_v1', __name__)


@api_v1_bp.route('/articles', methods=['GET', 'POST'])
@jwt_required()
def protected_articles():
    current_user = get_jwt_identity()

    if request.method == 'GET':
        if not request.is_json:
            return "Unsupported Media Type: Expecting JSON", 415
        category = request.args.get('category', default='')
        limit = request.args.get('limit', default=15, type=int)
        page = request.args.get('page', default=1, type=int)

        # Вычисляем смещение на основе номера страницы
        offset = (page - 1) * limit

        query = """
            SELECT 
                articles.id, 
                articles.title, 
                articles.created_at, 
                articles.image_link, 
                themes.theme_name,
                json_agg(tags.tag_name) AS tags
            FROM 
                articles
            LEFT JOIN 
                themes ON articles.theme_id = themes.theme_id
            LEFT JOIN 
                article_tags ON articles.id = article_tags.article_id
            LEFT JOIN 
                tags ON article_tags.tag_id = tags.tag_id
        """

        if category:
            query += " WHERE themes.theme_name = %s"
        query += " GROUP BY articles.id, themes.theme_name"
        query += " ORDER BY articles.created_at DESC"
        query += " LIMIT %s OFFSET %s;"

        with psycopg2.connect(articles_connection) as connection:
            with connection.cursor() as cursor:
                try:
                    if category:
                        cursor.execute(query, (category, limit, offset))
                    else:
                        cursor.execute(query, (limit, offset))
                    articles = cursor.fetchall()
                    return jsonify(articles)
                except psycopg2.Error as err:
                    return f"Database error: {err}", 500

    if request.method == 'POST':
        if request.is_json:
            requested_data = request.get_json()
            data = Article(
                title=requested_data['title'],
                author=requested_data["author"],
                post_href=requested_data["post_href"],
                body=requested_data["body"],
                image_href=requested_data["image_href"]
            )
            with psycopg2.connect(articles_connection) as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(DB_INSERT_TABLE_ARTICLES,
                                    (data.title, data.author, data.post_href, data.body, data.image_href))
                        connection.commit()
                        article_id = cursor.fetchone()[0]
                    except psycopg2.Error as err:
                        connection.rollback()
                        return f"Article already exists! {err}", 500

                return {
                    "id": article_id,
                    "message": f"Article title:{data.title}, author:{data.author}, article href:{data.post_href}, article body:{data.body}, image href:{data.image_href}"
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
        if request.is_json:
            requested_data = request.get_json()
            data = Annotation(
                id=requested_data['id'],
                title=requested_data['title'],
                created_at=requested_data['created_at'],
                source_link=requested_data['source_link'],
                image_link=requested_data['image_link'],
                body=requested_data['body'],
                theme_name=requested_data['theme_name'],
                tags=requested_data['tags'],
                annotation=requested_data.get('annotation'),
                language_code=requested_data['language_code']
            )
            # print(data)
            query_annotation = """
                INSERT INTO annotations (article_id, annotation, language_code)
                VALUES (%s, %s, %s)
            """
            with psycopg2.connect(articles_connection) as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(query_annotation, (data.id, data.annotation, data.language_code))

                        # Insert theme if it doesn't exist and get its theme_id
                        theme_id = insert_theme(data.theme_name, cursor)

                        print(theme_id)
                        # Insert article-theme relationship
                        upadate_article_theme(data.id, theme_id, cursor)

                        # Insert tags if they don't exist and get their tag_ids
                        tag_ids = insert_tags(data.tags, cursor)

                        # Insert article-tag relationships into the article_tags table
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
                
def upadate_article_theme(article_id, theme_id, cursor):
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



@api_v1_bp.route('/articles/<uuid:article_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def article_api_by_id(article_id):
    current_user = get_jwt_identity()

    if request.method == 'GET':
        article_id = str(article_id)

        query = """
            SELECT 
                articles.id, 
                articles.title, 
                articles.created_at,
                articles.source_link,  
                articles.image_link,
                articles.body, 
                themes.theme_name,
                json_agg(tags.tag_name) AS tags,
                annotations.annotation,
                annotations.language_code
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
            WHERE 
                articles.id = %s
            GROUP BY 
                articles.id, themes.theme_name, annotations.annotation, annotations.language_code;
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

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass