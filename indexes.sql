-- Indexes on Foreign Keys for better query performance
CREATE INDEX idx_supplier_nationkey ON SUPPLIER(S_NATIONKEY);

CREATE INDEX idx_partsupp_partkey ON PARTSUPP(PS_PARTKEY);
CREATE INDEX idx_partsupp_suppkey ON PARTSUPP(PS_SUPPKEY);

CREATE INDEX idx_customer_nationkey ON CUSTOMER(C_NATIONKEY);

CREATE INDEX idx_orders_custkey ON ORDERS(O_CUSTKEY);

CREATE INDEX idx_lineitem_orderkey ON LINEITEM(L_ORDERKEY);
CREATE INDEX idx_lineitem_partkey_suppkey ON LINEITEM(L_PARTKEY, L_SUPPKEY);

CREATE INDEX idx_nation_regionkey ON NATION(N_REGIONKEY);
