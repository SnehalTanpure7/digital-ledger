from flask import Flask, render_template, request, redirect, url_for,session,flash
from function import customeradd,addUdhhar,add_payment,get_all_customers,get_by_customer_id,customer_udhar_history,total_udhar_amount,total_payment_amount,pending_history,update_customer,get_all_completedcustomers,get_all_pendingcustomers,total_count_customer,total_count_completedcustomer,total_pending_customer,total_pending_amount,get_all_history,shopkeeper_login,get_shopkeeper_by_id,update_profile,change_password

app = Flask(__name__)
app.secret_key = "smartkhata"
@app.route("/index.html",methods=["GET","POST"])
def index():
    if session.get('shopkeeper_logged_in'):
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        shopkeeper=shopkeeper_login(email,password)
        if shopkeeper:
            session['shopkeeper_logged_in'] = True
            session['shopkeeper_id'] = shopkeeper['id']
            session['shopkeeper_name'] = shopkeeper['shopkeeper_name']
            session['shop_name'] = shopkeeper['shop_name']

            flash("Login Successfully", "success")

            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password", "error")

            return redirect(url_for("index"))
    return render_template("index.html")

# @app.route("/customers.html", methods=["GET", "POST"])
# def customers():
#     customer_id = request.form.get("customer_id")
#     if request.method == "POST":
#         name = request.form.get("name")
#         mobile = request.form.get("mobile")
#         customeradd(name, mobile)
#         return redirect(url_for("customers"))
#     customers=get_all_customers()
#     customer_update=update_customer(customer_id)
#     return render_template("customers.html",customers=customers,customer_update=customer_update)

@app.route("/customers.html", methods=["GET", "POST"])
def customers():
    if not session.get('shopkeeper_logged_in'):
            return redirect(url_for("index"))
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        if customer_id:
            update_customer(customer_id)
            flash("Customer updated successfully!", "success")
        else:
            name = request.form.get("name")
            mobile = request.form.get("mobile")
            customeradd(name, mobile)
            flash("Customer added successfully!", "success")
        return redirect(url_for("customers"))
    customers = get_all_customers()
    return render_template("customers.html", customers=customers)
@app.route("/customer-detail.html/<int:customer_id>", methods=["GET", "POST"])
def customers_detail(customer_id):
    if not session.get('shopkeeper_logged_in'):
            return redirect(url_for("index"))
    customer = get_by_customer_id(customer_id)
    if not customer:
        return "Customer not found", 404
    if request.method == "POST":
        item_name = request.form.get("item_name")
        quantity = request.form.get("quantity")
        price = request.form.get("price")
        due_date = request.form.get("due_date")
        addUdhhar(customer_id,item_name,quantity,price,due_date)
        flash("Udhaar added successfully!", "success")
        return redirect(url_for("customers_detail",customer_id=customer_id))
    customer_udhar=customer_udhar_history(customer_id)
    total_udhar=total_udhar_amount(customer_id)
    total_payment=total_payment_amount(customer_id)
    current_pending=total_udhar-total_payment
    pendinghistory=pending_history(customer_id)
    return render_template("customer-detail.html",customer=customer,customer_id=customer_id,customer_udhar=customer_udhar,total_udhar=total_udhar,total_payment=total_payment,current_pending=current_pending,pendinghistory=pendinghistory)

@app.route("/record-payment", methods=["POST"])
def record_payment():
    if not session.get('shopkeeper_logged_in'):
        return redirect(url_for("index"))
    customer_id = request.form["customer_id"]
    payment_amount = float(request.form["amount"])
    add_payment(customer_id, payment_amount)
    flash("Payment added successfully!", "success")
    return redirect(url_for("customers_detail", customer_id=customer_id))
@app.route("/dashboard.html")
def dashboard():
    if not session.get('shopkeeper_logged_in'):
        return redirect(url_for("index"))
    totalcustomer=total_count_customer()
    totalcompletedcustomer=total_count_completedcustomer()
    totalpendingcustomer=total_pending_customer()
    totalpendingamount=total_pending_amount()
    return render_template("dashboard.html",totalcustomer=totalcustomer,totalcompletedcustomer=totalcompletedcustomer,totalpendingcustomer=totalpendingcustomer,totalpendingamount=totalpendingamount)
@app.route("/profile.html", methods=["GET", "POST"])
def profile():
    shopkeeper_id = session.get("shopkeeper_id")
    if not shopkeeper_id:
        return redirect(url_for("index"))
    if request.method == "POST":
        shopkeeper_name = request.form.get("shopkeeper_name")
        shop_name = request.form.get("shop_name")
        mobile_number = request.form.get("mobile_number")
        email = request.form.get("email")
        # Check karo values aa rahi hain ya nahi
        print("Shopkeeper Name:", shopkeeper_name)
        print("Shop Name:", shop_name)
        print("Mobile:", mobile_number)
        print("Email:", email)
        update_profile(
            shopkeeper_id,
            shopkeeper_name,
            shop_name,
            mobile_number,
            email)
        flash("Profile updated successfully.", "success")

        return redirect(url_for("profile"))

    shopkeeper = get_shopkeeper_by_id(shopkeeper_id)

    return render_template(
        "profile.html",
        shopkeeper=shopkeeper)
@app.route("/changepassword.html",methods=["GET","POST"])
def changepassword():
    if not session.get('shopkeeper_logged_in'):
        return redirect(url_for("index"))
    shopkeeper_id = session.get("shopkeeper_id")
    if request.method == "POST":
        current_password = request.form.get("currentPassword")
        new_password = request.form.get("newPassword")
        confirm_password = request.form.get("confirmPassword")
        if not current_password or not new_password or not confirm_password:
            flash("Please fill all password fields.", "danger")
            return redirect(url_for("changepassword"))
        if new_password != confirm_password:
            flash("New Password and Confirm Password do not match.", "danger")
            return redirect(url_for("changepassword"))
        if current_password == new_password:
            flash("New Password cannot be the same as Current Password.", "warning")
            return redirect(url_for("changepassword"))
        changepass=change_password(shopkeeper_id,current_password,new_password)
        if changepass:
            flash("Password changed successfully.", "success")
        else:
            flash("Current Password does not match.", "danger")
        return redirect(url_for("changepassword"))
    return render_template("changepassword.html")

@app.route("/pending.html")
def pending():
    if not session.get('shopkeeper_logged_in'):
        return redirect(url_for("index"))
    pending_history=get_all_pendingcustomers()
    return render_template("pending.html",pending_history=pending_history)
@app.route("/notifications.html")
def notification():
    if not session.get('shopkeeper_logged_in'):
            return redirect(url_for("index"))
    return render_template("notifications.html")
@app.route("/history.html")
def history():
    if not session.get('shopkeeper_logged_in'):
            return redirect(url_for("index"))
    getallhistory=get_all_history()
    return render_template("history.html",getallhistory=getallhistory)

@app.route("/completed.html")
def completed():
    if not session.get('shopkeeper_logged_in'):
            return redirect(url_for("index"))
    completed_customer=get_all_completedcustomers()
    return render_template("completed.html",completed_customer=completed_customer)

if __name__ == "__main__":
    app.run(debug=True)