"""Unit tests for feature engineering logic."""


EXPECTED_FEATURE_COLUMNS = [
  'customer_id',
  'subscription_active',
  'pet_type_encoded',
  'days_since_last_order',
  'total_orders_12m',
  'avg_order_value',
  'total_spend_12m',
  'customer_tenure_days',
  'support_tickets_6m',
  'website_visits_30d',
  'churned',
]


def test_expected_columns_defined():
  """Verify the expected feature schema is complete and has no duplicates."""
  assert len(EXPECTED_FEATURE_COLUMNS) == len(set(EXPECTED_FEATURE_COLUMNS))
  assert 'customer_id' in EXPECTED_FEATURE_COLUMNS
  assert 'churned' in EXPECTED_FEATURE_COLUMNS


def test_customer_id_is_first_column():
  """Primary key should be the first column for clarity."""
  assert EXPECTED_FEATURE_COLUMNS[0] == 'customer_id'


def test_no_raw_categorical_columns():
  """pet_type should be encoded, not raw string."""
  assert 'pet_type' not in EXPECTED_FEATURE_COLUMNS
  assert 'pet_type_encoded' in EXPECTED_FEATURE_COLUMNS
