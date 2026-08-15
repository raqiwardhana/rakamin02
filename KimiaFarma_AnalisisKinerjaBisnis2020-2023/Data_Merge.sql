
CREATE TABLE Rakamin_KF_Analytics AS
SELECT 
    f.transaction_id AS trans_id,
    f.date,
    b.branch_id,
    b.branch_name,
    b.kota,
    b.provinsi AS prov,
    b.rating AS branch_rating,
    f.customer_name,
    p.product_id AS prod_id,
    p.product_name AS prod_name,
    f.price AS actual_price,
    f.discount_percentage,
    CASE 
        WHEN f.price <= 50000 THEN 0.10
        WHEN f.price > 50000 AND f.price <= 100000 THEN 0.15
        WHEN f.price > 100000 AND f.price <= 300000 THEN 0.20
        WHEN f.price > 300000 AND f.price <= 500000 THEN 0.25
        ELSE 0.30
    END AS gross_profit_percentage,
    (f.price * (1 - f.discount_percentage / 100.0)) AS nett_sales,
    ((f.price * (1 - f.discount_percentage / 100.0)) * 
    CASE 
        WHEN f.price <= 50000 THEN 0.10
        WHEN f.price > 50000 AND f.price <= 100000 THEN 0.15
        WHEN f.price > 100000 AND f.price <= 300000 THEN 0.20
        WHEN f.price > 300000 AND f.price <= 500000 THEN 0.25
        ELSE 0.30
    END) AS nett_profit,
    f.rating AS trans_rating
FROM "Final_Trans" f
JOIN "Branch" b ON CAST(f.branch_id AS VARCHAR) = CAST(b.branch_id AS VARCHAR)
JOIN "Prod" p ON CAST(f.product_id AS VARCHAR) = CAST(p.product_id AS VARCHAR)
LEFT JOIN "Invent" i ON CAST(f.branch_id AS VARCHAR) = CAST(i.branch_id AS VARCHAR) 
                   AND CAST(f.product_id AS VARCHAR) = CAST(i.product_id AS VARCHAR);