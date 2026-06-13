**Known Limits:** Requires valid `BOT_TOKEN` and `BOT_CHAT_ID` in `.env`. Without them, alerts silently fail (logged to console).

### Favorite Categories

**Overview:** Mark categories as favorites for quick access.

**Design Decisions:** Added `is_favorite` boolean field to Category model. No separate endpoint needed; just include in the category list response.

**API Changes:**
- Added `is_favorite` field to Category model and CategorySerializer

**Example Request/Response:**
```json
POST /api/categories/
{
  "name": "Shopping",
  "is_favorite": true
}

HTTP 201 Created
{
  "id": 3,
  "user": "testuser",
  "name": "Shopping",
  "is_favorite": true
}
```

**Known Limits:** Frontend must filter favorites client-side; no dedicated "favorites-only" endpoint yet.

### Monthly Spending Summaries

**Overview:** View total spending grouped by month.

**Design Decisions:** New endpoint `/api/expenses/monthly-summary/` uses Django's `TruncMonth()` function to group expenses by month. Returns a simple list of month-total pairs.

**API Changes:**
- Added new endpoint `monthly_summary()` view
- New URL pattern: `/api/expenses/monthly-summary/`

**Example Request/Response:**
```json
GET /api/expenses/monthly-summary/

HTTP 200 OK
{
  "base_currency": "USD",
  "monthly": [
    {
      "month": "2026-06",
      "total": "180"
    }
  ]
}
```

**Known Limits:** Does not convert currencies. Shows totals in original currency.

---

## Bugs Found and Fixed

### Bug 1: Typo in serializers.py field name
**Description:** CategorySerializer had `catgory` instead of `category`.
**Root Cause:** Typo when defining the serializer.
**Fix:** Changed `"catgory"` to `"category"` in the field list.
**Commit Hash:** (Run `git log --oneline` and find the commit for this fix)

### Bug 2: Typo in views.py variable name
**Description:** `expense_list()` view used `serialzer` instead of `serializer`.
**Root Cause:** Typo in variable assignment.
**Fix:** Changed `serialzer` to `serializer`.
**Commit Hash:** (Run `git log --oneline` and find the commit for this fix)

### Bug 3: Wrong date filter operator
**Description:** `expense_list()` used `date__gt` instead of `date__gte` for start_date filtering, excluding the start date itself.
**Root Cause:** Incorrect lookup used; should be inclusive.
**Fix:** Changed `date__gt` to `date__gte`.
**Commit Hash:** (Run `git log --oneline` and find the commit for this fix)

### Bug 4: Missing import
**Description:** `expense_summary()` used `Sum()` but didn't import it.
**Root Cause:** Import statement was missing.
**Fix:** Added `from django.db.models import Sum`.
**Commit Hash:** (Run `git log --oneline` and find the commit for this fix)

### Bug 5: Wrong response key in summary
**Description:** `expense_summary()` returned `category__name` as the key instead of `category`.
**Root Cause:** Used the ORM field name instead of the desired response key.
**Fix:** Transformed the response to use `"category"` as the key with renamed dict comprehension.
**Commit Hash:** (Run `git log --oneline` and find the commit for this fix)