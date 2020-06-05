from flask import *
#test
import secrets,sqlite3,hashlib,os,base64,json
App = Flask(__name__)
class data:
	def __init__(self, pas=None, text=None, id=None):
		self.text=text
		self.pas = pas
		self.id  = id
	def buat(self):
		sql = sqlite3.connect('data.db')
		db = sql.cursor()
		db.execute('INSERT INTO SC VALUES ("%s","%s","%s")'%(self.pas,self.id,self.text))
		sql.commit()
		sql.close()
		return 'p'
	def cari(self):
		sql=sqlite3.connect('data.db')
		db = sql.cursor()
		dump=db.execute('SELECT * FROM SC WHERE PAS="%s" AND ID="%s"'%(self.pas,self.id)).fetchall()
		sql.commit()
		sql.close()
		return base64.b64decode(dump[0][2])
@App.route('/',methods=['POST','GET'])
def index():
	if request.method == 'POST':
		if ( request.form.get('pass') and request.form.get('text') ):
			id=secrets.token_hex(8)
			x=data(pas=hashlib.md5(bytes(request.form.get('pass').encode())).hexdigest(),text=base64.b64encode(request.form.get('text').encode()).decode())
			x.buat()
			return {'status':'sukses','id':id,'password':request.form.get('pass'),'url':'https://kpt55-scripts.herokuapp.com/?id=%s&pass=%s'%(id,request.form.get('pass'))}
		else:
			return {'status':'gagal'}
	else:
		if request.args.get('pass') and request.args.get('id'):
			db=data(pas=hashlib.md5(request.args.get('pass').encode()).hexdigest(),id=request.form.get('id'))
			if db.cari():
				return db.cari()
			else:
				return {'status':'error','pesan':'pass & id salah'}
		else:
			return render_template('index.html')
if __name__ == '__main__':
	App.run(host='0.0.0.0',port=int(os.environ.get('PORT','5000')), debug=True)
