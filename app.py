from main import *


#LOGIN
@app.route('/', methods=['GET','POST'])
def login():
    if request.form:
        session['username'] = request.form['username']
        password = request.form['password']
        session['login']=False
        user = mongo.db.users.count({'username':session['username'],'password':password})
        val = mongo.db.users.find_one({'username':session['username'],'password':password})
        print(user)
        session['iduser'] = val['_id']
        print(session['iduser'])
        if user > 0 :
            session['login'] = True
            return redirect(url_for('memberDashboard'))
        else:
            return render_template('login.html')
    return render_template('login.html')


#ADMIN HOME
@app.route('/home', methods=['GET','POST'])
def memberDashboard():
    if session['login'] == True:
        findUsr = mongo.db.users.find_one({'username':session['username']})
        print(findUsr['username'])
        events= mongo.db.events.find({})
        return render_template('admin/allEvent.html',event=events)
    elif session['login'] == False:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

#LOGOUT
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('login', False)
   return redirect(url_for('login'))




#REGISTER - Operator
@app.route('/register', methods=['GET', 'POST'])
def registOperator():
    data = request.form
    today = str(date.today())
    allEdt = mongo.db.users.count({})
    aut = allEdt + 1
    autic = 'USR'+str(aut)
    if request.form:
        userid = autic
        name = data['nama']
        email = data['email']
        username = data['username']
        password = data['password']
        noHp = data['nohp']
        jk = data['gender']
        alamat = data['alamat']
        newUser = mongo.db.users.insert({
            '_id':userid,
            'foto':'default.jpg',
            'nama':name,
            'email':email,
            'username':username,
            'password':password,
            'noHp':noHp,
            'gender':jk,
            'alamat':alamat,
            'verified':False,
            'createdAt':today,
            'updatedAt':today,
            'deleted':False
            })
        if newUser and request.method=='POST':
            return 'Success!'
        else:
            return 'Error!'
    return render_template('register.html')








def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#NEW EVENT
@app.route('/new/event', methods=['GET', 'POST'])
def newEvent():
    if session['login'] == True:
        events= mongo.db.events.find({})
        data = request.form
        today = str(date.today())
        allEdt = mongo.db.events.count({})
        aut = allEdt + 1
        autic = 'EVNT'+str(aut)
        if request.form:
            eventId = autic
            name = data['eventName']
            if 'image' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['image']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ctgr = data['categori']
            prmtr = data['promotor']
            mulai = data['waktuMulai']
            if request.method=='POST':
                NewEvent = mongo.db.events.insert({
                    '_id':eventId,
                    'name':name,
                    'foto':file.filename,
                    'categori':ctgr,
                    'promotor':prmtr,
                    'tanggalMulai':mulai,
                    'createdAt':today,
                    'updatedAt':today,
                    'delete':False
                })
                return redirect(url_for('newEvent'))
            else:
                return 'Error 404'
        allEvnt= mongo.db.events.find({})
        return render_template('admin/newEvent.html',event=allEvnt)
    elif session['login'] == False:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

#ALL EVENT - ADMIN
@app.route('/all/event', methods=['GET','POST'])
def allEvnt():
    data = mongo.db.events.find()
    return render_template('admin/allEvent.html', data=data)




#DETAIL EVENT
@app.route('/detail/<idevnt>',methods=['POST','GET'])
def detEvnt(idevnt):
    if session['login'] == True:
        evnt = mongo.db.events.find_one({'_id':idevnt})
        return render_template('admin/detailEvent.html', event=evnt)
    elif session['login'] == False:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))






#DELETE EVENT - ADMIN
@app.route('/delete/event/<_id>/<name>',methods=['GET','DELETE'])
def deletEvnt(_id,name):
    mongo.db.events.remove({'_id':_id,'name':name})
    return redirect(url_for('allEvnt'))
    








#EDIT EVENT - ADMIN
@app.route('/edit/event/<_id>/<name>', methods=['GET','POST'])
def editEvnt(_id,name):
    data = mongo.db.events.find_one({'_id':_id,'name':name})
    return render_template('admin/editEvent.html',data=data)




#ABSEN
@app.route('/absen/event/<event>',methods=['GET','POST'])
def attend(event):
    allEdt = mongo.db.absen.count()
    aut = allEdt + 1
    autic = 'ABS'+str(aut)
    data = request.form
    if request.method == 'POST':
        nis = data['nis']
        check = mongo.db.siswa.count({'nis':nis})
        if check > 0:
            dd = mongo.db.siswa.find_one({'nis':nis})
            print(dd['nama'])
            mongo.db.absen.insert({
            '_id':autic,
            'eventId':event,
            'nis':nis,
            'nama': dd['nama'],
            'rombel':dd['rombel'],
            'rayon':dd['rayon'],
            'jk':dd['jk'],
            'foto':dd['foto']
            })
            print('success')
        else:
            return 'Notfound'
    return render_template('admin/index.html')



#UPDATE MEMBER
@app.route('/new/member', methods=['GET','POST'])
def regMember():
    allEdt = mongo.db.siswa.count({})
    aut = allEdt + 1
    autic = 'STD'+str(aut)
    dict = {}
    with open('siswa.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            print(row['nis'], row['rombel'])
            gettype = mongo.db.siswa.count({'_id':row['_id']})
            print(gettype)
            if gettype > 0:
                mongo.db.siswa.update({'_id':row['_id']},{
                'nis':row['nis'],
                'nama':row['nama'],
                'rombel':row['rombel'],
                'rayon':row['rayon'],
                'jk':row['jk'],
                'foto':row['foto'],
                })
                print('Updated')
                flash('Success')
            else:
                dict['_id'] = row['_id']
                dict['nis'] = row['nis']
                dict['nama'] = row['nama']
                dict['rombel'] = row['rombel']
                dict['rayon'] = row['rayon']
                dict['jk'] = row['jk']
                dict['foto'] = row['foto']
                print('else')
                print(dict)
                mongo.db.siswa.insert(dict)
        return jsonify({'success':True})




if __name__ == '__main__':
    app.run(debug=True)