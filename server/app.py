from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS


from models import db, Chama, Member, Contribution, membership


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chama.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


CORS(app)
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)

# Resources
class ChamaListResource(Resource):
	def get(self):
		return [c.to_dict() for c in Chama.query.all()]

	def post(self):
		data = request.json
		if not data.get('name') or len(data['name']) < 2:
			return {'error': 'Chama name required, min length 2'}, 400
		if Chama.query.filter_by(name=data['name']).first():
			return {'error': 'Chama with that name exists'}, 400
		chama = Chama(name=data['name'], description=data.get('description'))
		db.session.add(chama)
		db.session.commit()
		return chama.to_dict(), 201

class ChamaResource(Resource):
	def get(self, chama_id):
		return Chama.query.get_or_404(chama_id).to_dict()

class MemberListResource(Resource):
	def get(self):
		return [m.to_dict() for m in Member.query.all()]

	def post(self):
		data = request.json
		if not data.get('name'):
			return {'error': 'Name required'}, 400
		if not data.get('email') or '@' not in data['email']:
			return {'error': 'Valid email required'}, 400
		if Member.query.filter_by(email=data['email']).first():
			return {'error': 'Member with that email exists'}, 400
		member = Member(name=data['name'], email=data['email'], phone=data.get('phone'))
		db.session.add(member)
		db.session.commit()
		return member.to_dict(), 201

class MemberResource(Resource):
	def get(self, member_id):
		return Member.query.get_or_404(member_id).to_dict()
class JoinChamaResource(Resource):
    def post(self, member_id, chama_id):
        member = Member.query.get_or_404(member_id)
        chama = Chama.query.get_or_404(chama_id)

        if chama in member.chamas:
            return {'message': 'Member already in chama'}, 200

        member.chamas.append(chama)
        db.session.commit()
        return {'message': 'Member added to chama'}


class ContributionListResource(Resource):
    def get(self):
        return [c.to_dict() for c in Contribution.query.order_by(Contribution.date.desc()).all()]

    def post(self):
        data = request.json
        if not isinstance(data.get('amount'), (int, float)) or data['amount'] <= 0:
            return {'error': 'Valid amount required'}, 400

        member = Member.query.get(data.get('member_id'))
        chama = Chama.query.get(data.get('chama_id'))

        if not member or not chama:
            return {'error': 'Member or Chama not found'}, 404

        if chama not in member.chamas:
            return {'error': 'Member must join chama before contributing'}, 400

        contrib = Contribution(
            amount=data['amount'],
            note=data.get('note'),
            member=member,
            chama=chama
        )
        db.session.add(contrib)
        db.session.commit()
        return contrib.to_dict(), 201

class ContributionResource(Resource):
    def get(self, contrib_id):
        return Contribution.query.get_or_404(contrib_id).to_dict()

    def put(self, contrib_id):
        contrib = Contribution.query.get_or_404(contrib_id)
        data = request.json

        if not isinstance(data.get('amount'), (int, float)) or data['amount'] <= 0:
            return {'error': 'Valid amount required'}, 400

        member = Member.query.get(data.get('member_id'))
        chama = Chama.query.get(data.get('chama_id'))

        if not member or not chama:
            return {'error': 'Member or Chama not found'}, 404

        if chama not in member.chamas:
            return {'error': 'Member must join chama before contributing'}, 400

        contrib.amount = data['amount']
        contrib.note = data.get('note')
        contrib.member = member
        contrib.chama = chama

        db.session.commit()
        return contrib.to_dict()

    def delete(self, contrib_id):
        contrib = Contribution.query.get_or_404(contrib_id)
        db.session.delete(contrib)
        db.session.commit()
        return '', 204


api.add_resource(ChamaListResource, '/api/chamas')
api.add_resource(ChamaResource, '/api/chamas/<int:chama_id>')
api.add_resource(MemberListResource, '/api/members')
api.add_resource(MemberResource, '/api/members/<int:member_id>')
api.add_resource(JoinChamaResource, '/api/members/<int:member_id>/join/<int:chama_id>')
api.add_resource(ContributionListResource, '/api/contributions')
api.add_resource(ContributionResource, '/api/contributions/<int:contrib_id>')

@app.route('/')
def home():
    return {'msg': 'Chama backend running with Alembic + SerializerMixin'}


if __name__ == '__main__':
    app.run(debug=True)
		