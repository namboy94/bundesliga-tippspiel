"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bundesliga-tippspiel.

bundesliga-tippspiel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bundesliga-tippspiel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from typing import Optional
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from puffotter.flask.base import db
from bundesliga_tippspiel.db.user_generated.ChatMessage import ChatMessage


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/chat", methods=["GET"])
    @blueprint.route("/chat/<int:page>", methods=["GET"])
    @login_required
    def chat(page: Optional[int] = 1):
        """
        Displays the chat page
        :param page: The page of the chat to display
        :return: The response
        """
        chat_messages = ChatMessage.query.all()
        chat_messages.sort(key=lambda x: x.creation_time, reverse=True)
        return render_template(
            "chat/chat.html",
            messages=chat_messages
        )

    @blueprint.route("/new_chat_message", methods=["POST"])
    @login_required
    def new_chat_message():
        """
        Places a new chat message
        :return: The response
        """
        text = request.form["text"]
        parent_id = request.form.get("parent_id")
        message = ChatMessage(
            user=current_user, text=text, parent_id=parent_id
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("chat.chat"))

    @blueprint.route("/delete_chat_message/<int:message_id>", methods=["POST"])
    @login_required
    def delete_chat_message(message_id: int):
        """
        Deletes a chat message
        :param message_id: The ID of the message to delete
        :return: The response
        """
        message = ChatMessage.query.get(message_id)
        if message is not None and message.user_id == current_user.id:
            message.delete()
            db.session.commit()
            flash("Kommentar wurde gelöscht", "success")
        else:
            flash("Kommentar konnte nicht gelöscht werden", "danger")
        return redirect(url_for("chat.chat"))

    return blueprint