SELECT SUM(c.quantity)
FROM cart_items c JOIN product p on c.product_id = p.id
WHERE p.name = 'Guitar'