from flask import Flask,render_template,request,jsonify,send_from_directory
import pickle
import passwordstrength
from sklearn.feature_extraction.text import TfidfVectorizer


def getTokens(inputString):
    tokens = []
    for i in inputString:
    # i = i.astype('u')
        tokens.append(i)
    # print(tokens)
    return tokens


app = Flask(__name__)


'''
@app.route('/')
def home():
    return render_template('home.html')
'''

model = pickle.load(open('model.pk1','rb'))

vectorizer = pickle.load(open('vector.pk1','rb'))

class ml_passwordstrength:
    def __init__(self, password):
        self.password = []
        self.password.append(password)
        
        self.score = self.__classification_score()[0] + 1
        
    
    def __classification_score(self):
        vect_password = vectorizer.transform(self.password)
        return model.predict(vect_password) 
    
    def get_ml_score(self):
        return self.score

@app.route('/',methods=['GET','POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    password_value = ""
    if request.method == 'POST':
        password_value = request.form['pwd']
    password = passwordstrength.passwordstrength(password_value)
    ml_password = ml_passwordstrength(password_value)
    password_score = password.get_score()
    ml_password_score = ml_password.get_ml_score()

    results = password.get_results()
    flags = password.get_strength_flags()

    password_score = password_score if password_score <= 100 else 100


    if ml_password_score == 1:
        ml_password_score = 25
    elif ml_password_score == 2:
        ml_password_score = 60
    elif ml_password_score == 3:
        ml_password_score = 100
    
    final_score = (password_score + ml_password_score) / 2

    return render_template('index.html',password_value = password_value,final_score = final_score, results = results, flags = flags)

@app.route('/report')
def report():
    filepath = 'static/Report.pdf'
    return send_from_directory(app.config['UPLOAD_FOLDER'], filepath,as_attachment = True)


if __name__ == "__main__":
    app.run(debug=False)