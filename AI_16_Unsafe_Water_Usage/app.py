from flask import Flask, render_template, request
from flask import render_template
import matplotlib.pyplot as plt
from pandas import read_csv
import seaborn as sns
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config['SECRET_KEY'] = '123'

#create dropdown list to select the countries
cr = read_csv('Country_Region_List.csv')
countries = cr.Region.to_list()

class Form(FlaskForm):
    country1 = SelectField('Country_1', choices=countries)
    country2 = SelectField('Country_2', choices=countries)
    country3 = SelectField('Country_3', choices=countries)
    country4 = SelectField('Country_4', choices=countries)
    country5 = SelectField('Country_5', choices=countries)
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = Form()
    return render_template('home.html',form=form)

#Create the boxplot for the selected countries
sns.set(rc={'figure.figsize':(11.7, 6.57)})
sns.set(style="ticks")

plt.grid(True, which="both")

@app.route("/show_boxplot", methods=['GET', 'POST'])
def show():
    country1=request.form.get("country1")
    country2=request.form.get("country2")
    country3=request.form.get("country3")
    country4=request.form.get("country4")
    country5=request.form.get("country5")

    df = read_csv('number-of-deaths-by-risk-factor.csv')
    df = df[['Country', 'Year', 'Deaths']]
    df = df[(df['Country'].isin([country1,country2,country3,country4,country5]))] 

    ax = sns.boxplot(x='Deaths', y='Country', data=df, width=0.85)

    plt.grid(True, which="both")
    ax.set_xscale("log")
    ax.set_xlabel("Number of Death / Year")
    ax.set_ylabel("Country / Region")
    ax.set_title("Number of Death Per Year Caused by Unsafe Water Usage\nin " +country1+", " +country2+", "+country3+", "+ country4+", and "+country5)
    
    png_name = "boxplot.png"
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(f'./static/{png_name}')
    fig.clf()
    
    return render_template("show.html")

if __name__ == "__main__":
    app.run(debug=True)