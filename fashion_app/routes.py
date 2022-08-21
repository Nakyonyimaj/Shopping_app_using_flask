from crypt import methods
from functools import total_ordering
from itertools import product
from flask_login import login_user, current_user, logout_user, login_required
from fashion_app import app , db ,bcrypt ,photos
from flask import redirect, render_template , redirect , url_for ,flash,send_from_directory , request , session
from fashion_app.forms import LoginForm, RegisterForm , AddItemsform , Categoryform
from fashion_app.models import AddItems, Category,  User 
import secrets
import os




@app.route('/')
@app.route('/home')
def home_page ():
    return render_template('home.html')


@app.route('/login', methods= ['GET','POST'])
def login_page ():
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            login_user(user)
            flash("You have successfully logged in")
            return redirect(url_for('market_page'))
        else:
            flash("Login invalid")
    else:
        print(form.errors)
    return render_template('login.html',form=form)


@app.route('/register',methods = ['GET','POST'])
def register_page ():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = User(username =form.username.data,email_address = form.email_address.data,password=form.password1.data)
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        flash(f'Your account has been successfully created',category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    
    return render_template('register.html' , form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/category',methods = ['GET','POST'])
def addcat():
    form = Categoryform()
    if request.method == 'POST':
        cat = Category(name = form.name.data)
        db.session.add(cat)
        db.session.commit()
        flash(f"{cat} was successfully added to categories", category='success')
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with adding a category: {err_msg}', category='danger')
    return render_template('addcat.html',form=form)

  
     
@app.route('/market')
def market_page ():

    page=request.args.get('page',1,type=int)
    products = AddItems.query.filter(AddItems.stock>0).paginate(page=page,per_page=3)
    categories = Category.query.join(AddItems,(Category.id == AddItems.category_id)).all()
    return render_template("market.html", products=products ,categories=categories)

@app.route('/categories/<int:id>')
def get_category(id):
    page=request.args.get('page',1,type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod =AddItems.query.filter_by(category=get_cat ).paginate(page=page,per_page=3)
    categories = Category.query.join(AddItems,(Category.id == AddItems.category_id)).all()
    return render_template("market.html", get_cat_prod=get_cat_prod ,categories=categories, get_cat=get_cat)
  

@app.route('/images/<filename>')
def get_file(filename):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"],filename)



@app.route('/product/<int:id>')
def single_page (id):
    product = AddItems.query.get_or_404(id)
    categories = Category.query.join(AddItems,(Category.id == AddItems.category_id)).all()
    return render_template("single.html", product=product,categories=categories)

    

@app.route('/addItems',methods= ['GET','POST'])
def addItems():
    
    form = AddItemsform()
    categories = Category.query.all()
    
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        description =form.description.data
        category = request.form.get('category')
        filename = photos.save(form.image_1.data)
        image_1=url_for('get_file',filename=filename)
        addproduct = AddItems(name=name,price=price,stock=stock, description=description ,category_id=category , image_1=image_1)
        db.session.add(addproduct)
        db.session.commit()
        flash(f"{name} was successfully added to products", category='success')
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with adding a product: {err_msg}', category='danger')
    return render_template('additems.html',form=form ,categories=categories )

        
@app.route('/itemTable') 
def itemTable_page():
    items = AddItems.query.filter(AddItems.stock>0)
    return render_template('item_table.html', items=items)


@app.route('/updateItems/<int:id>',methods=['GET','POST'])
def update_items_page(id):
    categories = Category.query.all()
    item=AddItems.query.get_or_404(id)
    category=request.form.get('category')
    form = AddItemsform(request.form)
    if request.method=="POST":
        item.name=form.name.data
        item.price = form.price.data
        item.stock = form.stock.data
        item.description =form.description.data
        item.category_id = category
        db.session.commit()
        flash(f'Item has sucessfully been updated',category='success')
    form.name.data=item.name
    form.price.data=item.price 
    form.description.data=item.description
    form.stock.data=item.stock
    return render_template('update_items.html', form=form,item=item, categories=categories)  



        
def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False      

@app.route('/addcart',methods=['POST'])       
def AddCart():
    try:
        product_id=request.form['product_id']
        quantity= request.form['quantity']
        product = AddItems.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method=='POST':
            DictItems={product_id:{'name':product.name,'price':product.price,'quantity':quantity,'image':product.image_1}} 
            all_total_price = 0
            all_total_quantity=0
            
            if 'cart' in session:
                if product_id in session['cart']:
                    flash('This is already in cart',category='success')
                            
                else:
                    session['cart'] = array_merge(session['cart'],DictItems)
                    return redirect(request.referrer)
                
            else:
                session['cart']=DictItems  
               
                return redirect(request.referrer)
        else:
            flash(f'Error while adding item to cart',category='danger')
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)           
        
        
@app.route('/cart')
def cart_page():
    if 'cart' not in session:
        return redirect(request.referrer)
    total = 0
    total_q=0
    g_total = 0
    qua = 0
    for key ,product in session['cart'].items():
        total += int(product['price'])* int(product['quantity'])
        total_q +=int(product['quantity'])
        g_total= total
        qua = total_q
        
    return render_template('cart.html',g_total=g_total,qua=qua)


      
@app.route('/empty')
def empty_cart():
 try:
    session.clear()
    return redirect(url_for('market_page'))
 except Exception as e:
     print(e)
 


@app.route('/delete/<int:id>')
def delete_product(id):
    if 'cart' not in session and len(session['cart']<=0):
        return redirect(url_for('market_page'))
    
    try:
        session.modified = True
   
        for key,product in session['cart'].items():
            if int(key) == id:    
                session['cart'].pop(key, None)
                return redirect(url_for('cart_page'))
            
    except Exception as e:
        print(e)
        return redirect(url_for('cart_page'))
    
@app.route('/updateCart/<int:id>',methods=['POST'])
def update_cart(id):
    if 'cart' not in session and len(session['cart'])<=0:
        return redirect(request.referrer)
    if request.method=='POST':
        quantity = request.form['quantity']
        try:
            session.modified=True
            for key,product in session['cart'].items():
                if int(key)== id:
                    product['quantity'] = quantity
                    flash('Product successfully update')
                    return redirect(url_for('cart_page'))
        except Exception as e:
            print(e)
            return redirect(url_for('cart_page'))            