"""seed_admin_user

Revision ID: 82efae84f694
Revises: 96c09015d01d
Create Date: 2025-12-24 21:02:39.781481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82efae84f694'
down_revision: Union[str, Sequence[str], None] = '96c09015d01d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO auth.users (
            instance_id,
            id,
            aud,
            role,
            email,
            encrypted_password,
            email_confirmed_at,
            confirmation_token,
            recovery_token,
            email_change_token_new,
            email_change,
            raw_app_meta_data,
            raw_user_meta_data,
            created_at,
            updated_at
        ) VALUES (
            '00000000-0000-0000-0000-000000000000',
            gen_random_uuid(),
            'authenticated',
            'authenticated',
            'admin@example.com',
            crypt('e3pass!', gen_salt('bf')),
            now(),
            '',
            '',
            '',
            '',
            '{"provider": "email", "providers": ["email"]}',
            '{}',
            now(),
            now()
        )
    """)

def downgrade():
    op.execute("DELETE FROM auth.users WHERE email = 'admin@example.com'")


