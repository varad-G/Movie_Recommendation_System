from flask import Flask , redirect , url_for , render_template , request , session  
import pandas as pd


ratings = pd.read_csv("ratings.csv")
ratings.head()

movies = pd.read_csv("movies.csv")
#print(movies["movieId"])

pivotTable = ratings.pivot_table(index=['userId'],columns=['movieId'],values='rating')
pivotTable.head()

corrTable=pivotTable.corr(min_periods=100)

corrTable.head()

def ItemsFromIDs (items,IDlist):
  df = pd.DataFrame(columns=items.columns)
  for id in IDlist:
    item = items[items.movieId ==id]
    df = pd.concat([df,item],axis=0)

  df.reset_index(inplace=True ,drop=True)
  return df

ItemsFromIDs(movies,[1,2])

def relatedRecos(itemName):
  MovieID = movies[movies.title==itemName]["movieId"].iloc[0]
  my_corr = corrTable.loc[MovieID]
  top10 = my_corr.dropna().sort_values(ascending=False)[:10]
  top10itemIDs = list(top10.index)
  top10items = ItemsFromIDs(movies, top10itemIDs)
  return top10items

#itemName = 'Toy Story (1995)'

#top10Recos=relatedRecos(itemName)
#top10Recos

#print(top10Recos['title'])


app = Flask(__name__)

app.secret_key = "varad"

@app.route("/", methods=["POST", "GET"])
def search():
    li = []
    if request.method == "POST":
        ip = request.form["fname"]
        top10Recos=relatedRecos(ip)
        for i in top10Recos["title"]:
            li.append(i)            
        session["home"] = li
        session["ip"] = ip
        return redirect(url_for("home"))
    else:
        return render_template("search.html")

@app.route("/result")
def home():  
    if "home" in session:
        home = session["home"]
        ip = session["ip"]
        return render_template("index.html", content=home, pro_name=ip)
    else:
        return (url_for("search"))
    
if __name__ == "__main__":
    app.run()






















