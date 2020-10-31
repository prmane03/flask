from flask import Flask,render_template,request, redirect, url_for
import requests

app = Flask(__name__)
col = {'green':['#8ebf42', '#82b534'],'blue':['#095484','#0666a3'], 'pink':['#a82877', '#bf1e81']}
quelist= []
queCount=0
	
@app.route('/form1')
def form1():
	try:
		if request.args.get("add"):
			if(str(request.args.get("mcqque"))!=''):
				que= request.args.get("mcqque")
				opt1= request.args.get("opt1")
				opt2= request.args.get('opt2')
				opt3= request.args.get("opt3")
				opt4= request.args.get("opt4")
				print("before MCQTYPE  : ",type(que),que)
				return redirect(url_for('add',mcqque=str(que),opt1=opt1,opt2=opt2,opt3=opt3,opt4=opt4))
			if(str(request.args.get("tfque"))!=''):
				que= request.args.get("tfque")
				print("before TFTYPE  : ",type(que),que)
				return redirect(url_for('add',tfque=str(que)))
		if request.args.get("clear"):
			return redirect(url_for('clear'))
	except :
		return "ERROR"


@app.route('/form2')
def form2():
	try:
		if request.args.get("preview"):
			title=request.args.get('title')
			theme=request.args.get("theme")
			return redirect(url_for('preview',title=str(title),theme=str(theme)))
		if request.args.get("generate"):
			title=request.args.get('title')
			theme=request.args.get("theme")
			return redirect(url_for('generate',title=str(title),theme=str(theme)))
	except :
		return "ERROR"

@app.route('/')
def index():
	return render_template('index.html',queCount=queCount)
	
@app.route('/add')	
def add():
	global queCount
	queCount+=1
	c=str(queCount)
	if(str(request.args.get("mcqque"))!='None'):
		que= str( request.args.get("mcqque"))
		opt1= str(request.args.get("opt1"))
		opt2= str(request.args.get('opt2'))	
		opt3= str(request.args.get("opt3"))	
		opt4= str(request.args.get("opt4"))
		query=""
		with open('mcq.txt','r') as f:
			query=f.read()
		print("MCQTYPE : ",type(que),que)
		quelist.append(query.format(c=c,que=que,opt1=opt1,opt2=opt2,opt3=opt3,opt4=opt4))
	if(str(request.args.get("tfque"))!='None'):
		que= str(request.args.get("tfque"))
		query=""
		with open('tf.txt','r') as f:
			query=f.read()
		print("TFTYPE  : ",type(que),que)
		quelist.append(query.format(c=c,que=que))
		
	return render_template('index.html',queCount=queCount)
	

@app.route('/clear')
def clear():
	global queCount
	global quelist
	global anslist
	queCount=0
	quelist=[]
	return render_template('index.html',queCount=queCount)

@app.route('/preview')
def preview():
	global queCount
	global anslist
	title= request.args.get('title')
	theme= request.args.get('theme')
	col1,col2 = col[theme]
	head=""
	with open('head.txt','r') as f:
		head=f.read()
	head= head.replace('&col1',col1,9)
	head= head.replace('&title',title,2)
	head= head.replace('&col2',col2)
	head= head.replace('&c',str(queCount),2)
	tail=""
	with open('tail.txt','r') as f:
		tail=f.read()
	return head+"".join(quelist)+tail
	

@app.route('/generate')
def generate():
	global queCount
	global anslist
	title= request.args.get('title')
	theme= request.args.get('theme')
	col1,col2 = col[theme]
	code=""
	head=""
	with open('head.txt','r') as f:
		head=f.read()
		print("title : ",title,"col1 : ",col1,"col2 : ",col2)
	head= head.replace('&col1',col1,9)
	head= head.replace('&title',title,2)
	head= head.replace('&col2',col2)
	head= head.replace('&c',str(queCount),2)
	tail=""
	with open('tail.txt','r') as f:
		tail=f.read()
	code=head+"".join(quelist)+tail
	with open("form.html","w") as f:
		f.write(code)
	return "<h1>Created</h1>"
	
	
if __name__=="__main__":
	app.run()
