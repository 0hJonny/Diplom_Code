import psycopg2
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from PostgreSQL import DB_INSERT_TABLE_ARTICLES
from utils.database import connection
from models.articles import Article

api_v1_bp = Blueprint('api_v1', __name__)


@api_v1_bp.route('/articles', methods=['GET', 'POST'])
@jwt_required()
def protected_articles():
    current_user = get_jwt_identity()

    if request.method == 'GET':
        return f"Hello, {current_user}! This is a protected resource.", 200

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
            with connection, connection.cursor() as cursor:
                try:
                    cursor.execute(DB_INSERT_TABLE_ARTICLES,
                                   (data.title, data.author, data.post_href, data.body, data.image_href))
                    connection.commit()
                    article_id = cursor.fetchone()[0]
                except psycopg2.Error as err:
                    return f"Article already exists! {err}", 500

            return {
                "id": article_id,
                "message": f"Article title:{data.title}, author:{data.author}, article href:{data.post_href}, article body:{data.body}, image href:{data.image_href}"
            }, 201
        else:
            return "Unsupported Media Type: Expecting JSON", 415
