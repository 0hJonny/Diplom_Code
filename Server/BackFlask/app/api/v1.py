import psycopg2
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from PostgreSQL import DB_INSERT_TABLE_ARTICLES
from utils.database import articles_connection
from models.articles import Article

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
                    finally:
                        connection.close()

                return {
                    "id": article_id,
                    "message": f"Article title:{data.title}, author:{data.author}, article href:{data.post_href}, article body:{data.body}, image href:{data.image_href}"
                }, 201
        else:
            return "Unsupported Media Type: Expecting JSON", 415


@api_v1_bp.route('/articles/<uuid:article_id>', methods=['GET, PUT, DELETE'])
@jwt_required()
def article_api_by_id(article_id):
    current_user = get_jwt_identity()

    if request.method == 'GET':
        query = """
            SELECT 
                articles.id, 
                articles.title, 
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
            WHERE 
                articles.id = %s
            GROUP BY 
                articles.id, themes.theme_name, annotations.annotation;
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