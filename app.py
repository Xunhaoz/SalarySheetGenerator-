# -*- coding: utf-8 -*-
import uuid
from modules.models import *
from scripts.id_card_processor import *
from scripts.pdf_generator import *
from modules.response import Response
from flask import Flask, render_template, redirect, url_for, request, send_from_directory

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

with app.app_context():
    # db.session.remove()
    # db.drop_all()
    db.create_all()


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    return Response.sever_error(e)


@app.route("/", methods=['GET'])
def index_table():
    members = db.session.execute(db.select(Member).order_by(Member.id)).scalars()
    return render_template("tables.html", members=members)


@app.route("/add_member", methods=['POST'])
def add_member():
    id_card_back = id_card_processed_pipline(request.files['id_card_back'])
    id_card_front = id_card_processed_pipline(request.files['id_card_front'])

    member = Member(
        name=request.form["name"],
        national_id=request.form["national_id"],
        phone=request.form["phone"],
        residence_address=request.form["residence_address"],
        mailing_address=request.form["mailing_address"],
        bank=request.form["bank"],
        bank_account=request.form["bank_account"],
        id_card_back=id_card_back,
        id_card_front=id_card_front
    )
    db.session.add(member)
    db.session.commit()
    return redirect(url_for('index_table'))


@app.route("/download_pdf", methods=['POST'])
def download_pdf():
    member = db.get_or_404(Member, request.form["member_id"])
    pdf_path = './static/asset/pdf/'
    file_name = f'{member.name}-勞務報酬簽收單.pdf'

    gen_pdf(
        member, request.form["project_name"], request.form["development_fee"], request.form["payment"],
        request.form["category"], request.form["method"], request.form["date"], pdf_path + file_name
    )

    return send_from_directory(pdf_path, file_name, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
