import requests
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash, Response
from models.api_requests import ApiRequests


app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/')
def home_page():
    return render_template('home.html')

 
#------------------------------------------------------------------------------------------------------------
#-----------------------> Category Templates
#------------------------------------------------------------------------------------------------------------


@app.route('/catalog')
def catalog_page():
    categories = ApiRequests.get_all_category_names()
    return render_template('catalog.html', categories=categories)


@app.route('/catalog/<string:category_from_url>/')
def single_category_page(category_from_url):
    category = ApiRequests.get_single_category(category_from_url)
    category_name = category[0]
    category_items = category[1]
    return render_template('single_category.html', category_name=category_name, category_items=category_items)


@app.route('/catalog/new', methods=['GET', 'POST'])
def post_new_category_page():
    if request.method == 'POST':
        new_category = request.form['name']
        ApiRequests.post_category(new_category)
        return redirect(url_for('catalog_page'))
    return render_template('post_new_category.html')


@app.route('/catalog/delete', methods=['GET', 'POST'])
def delete_category_page():
    if request.method == 'POST':
        bye_category = request.form['name']
        ApiRequests.delete_category(bye_category)
        return redirect(url_for('catalog_page'))
    return render_template('delete_category.html')


#------------------------------------------------------------------------------------------------------------
#-----------------------> Item Templates
#------------------------------------------------------------------------------------------------------------


@app.route('/catalog/items')
def all_items_page():
    r = requests.get("https://developer-catalog.herokuapp.com/catalog/items")
    data = r.json()
    items = data['items']
    name = []
    description = []
    category_id = []
    for item in items:
        name.append(item['name'])
        description.append(item['description'])
        category_id.append(item['category_id'])
    return render_template('all_items.html', items=items, name=name, description=description, category_id=category_id)


@app.route('/catalog/<int:category_id>/<string:item_from_url>/')
def get_single_item_page(category_id, item_from_url):
    data = ApiRequests.get_single_category_item(category_id, item_from_url)
    item_name = data['name']
    item_description = data['description']
    return render_template('single_category_item.html', item_name=item_name, item_description=item_description)


@app.route('/catalog/items/new', methods=['GET', 'POST'])
def post_new_item_page():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']
        ApiRequests.post_new_item(name, description, category_id)
        return redirect(url_for('all_items_page'))
    return render_template('post_new_item.html')

@app.route('/catalog/items/delete', methods=['GET', 'POST'])
def delete_item_page():
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        ApiRequests.delete_item(name, category_id)
        return redirect(url_for('all_items_page'))
    return render_template('delete_item.html')


@app.route('/catalog/items/edit', methods=['GET', 'POST'])
def edit_item_page():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']
        ApiRequests.edit_item(name, description, category_id)
        return redirect(url_for('all_items_page'))
    return render_template('edit_item.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
    app.run(port=5000)
