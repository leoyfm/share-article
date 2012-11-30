Answer 4
===============
See more details, please see the [schema.sql](https://github.com/HypnoticZoo/Round2-test/blob/master/schema.sql).
####1) Should put category in independent table <br />
It is obviously that using string to store categories is easy way to use and implement.
However, this method is hard to maintance. Because when you change the one of categories' name
you should update all the string to keep the consistency of category. That will cause the lots of
resouces on server when you have huge records. So the best way is that creating a table is to store categories 
and building a many to many between production table and category table.

####2) Add trigger on cart_items table
The benefit of add trigger is that the trigger can update cart table when you add new recodr in cart_items table.
In other words, the trigger can update cart's gst, net and gross when users add new item in their cart.
Moreover, when users delete some items from their cart, the record in cart table also can be update automatically.

####3) Create customer_cart view
This view combines the necessary information between customer table and cart table. The aim of this view is that 
customer_cart provides a convenience way to find the relationship between customers and their carts.

####4) Create invoice view
This view contains the information that required by invoice.

####5) Add trigger on customer table
Delete all cart's records that relate to this customer.

####6) Add trigger on cart table
Delete all cart_items' record that related to this cart.

