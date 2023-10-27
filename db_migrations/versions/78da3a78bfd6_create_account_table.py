"""create account table

Revision ID: 78da3a78bfd6
Revises: 
Create Date: 2023-09-29 10:07:16.968208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "78da3a78bfd6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("last_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("password_hash", sa.Text, nullable=False),
        sa.Column("address", JSONB),
        sa.Column("order_history", JSONB),
        sa.Column("wishlist", JSONB),
        sa.Column("cart", JSONB),
        sa.Column("user_type", sa.String(255)),
    )

    op.create_table(
        "vendors",
        sa.Column("vendor_id", sa.Integer, primary_key=True),
        sa.Column("vendor_name", sa.String(255), nullable=False),
        sa.Column("contact_info", JSONB),
        sa.Column("product_list", JSONB),
    )

    op.create_table(
        "categories",
        sa.Column("category_id", sa.Integer, primary_key=True),
        sa.Column("category_name", sa.String(255), nullable=False),
        sa.Column("parent_category", sa.Integer, nullable=True),
    )

    op.create_table(
        "products",
        sa.Column("product_id", sa.Integer, primary_key=True),
        sa.Column("product_name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("stock", sa.Integer, nullable=False),
        sa.Column("vendor_id", sa.Integer, sa.ForeignKey("vendors.vendor_id")),
        sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.category_id")),
        sa.Column("ratings_and_reviews", JSONB),
        sa.Column("product_details", JSONB),
    )

    op.create_table(
        "orders",
        sa.Column("order_id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("order_details", JSONB),
        sa.Column("shipping_address", JSONB),
        sa.Column("total_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("order_status", sa.String(255), nullable=False),
        sa.Column("payment_details", JSONB),
    )

    op.create_table(
        "order_details",
        sa.Column("order_detail_id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.order_id"), nullable=False),
        sa.Column("product_id", sa.Integer, sa.ForeignKey("products.product_id"), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("vendor_id", sa.Integer, sa.ForeignKey("vendors.vendor_id"), nullable=False),
        sa.Column("product_image", sa.String(255)),
        sa.Column("product_category", sa.String(255)),
    )

    op.create_table(
        "payments",
        sa.Column("payment_id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id")),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.order_id")),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("payment_method", sa.String(255), nullable=False),
        sa.Column("payment_status", sa.String(255), nullable=False),
    )

    op.create_table(
        "ratings_reviews",
        sa.Column("review_id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id")),
        sa.Column("product_id", sa.Integer, sa.ForeignKey("products.product_id")),
        sa.Column("rating", sa.Integer, nullable=False),
        sa.Column("review_text", sa.Text),
    )

    op.create_table(
        "shipping",
        sa.Column("shipping_id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.order_id")),
        sa.Column("shipping_method", sa.String(255), nullable=False),
        sa.Column("shipping_status", sa.String(255), nullable=False),
        sa.Column("tracking_number", sa.String(255)),
        sa.Column("estimated_delivery", sa.DateTime),
    )

    op.create_table(
        "promotions",
        sa.Column("promo_id", sa.Integer, primary_key=True),
        sa.Column("promo_code", sa.String(255), nullable=False),
        sa.Column("discount_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("valid_products", JSONB),
        sa.Column("expiry_date", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table("promotions")
    op.drop_table("shipping")
    op.drop_table("ratings_reviews")
    op.drop_table("payments")
    op.drop_table("order_details")
    op.drop_table("orders")
    op.drop_table("vendors")
    op.drop_table("categories")
    op.drop_table("products")
    op.drop_table("users")
