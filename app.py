from flask import Flask, render_template, request

app = Flask(__name__)

# ✅ Hardcoded companies
companies = [
    {"id": 1, "name": "Sheraspace"},
    {"id": 2, "name": "Lavish Interiors"},
    {"id": 3, "name": "Interior Concepts BD"},
    {"id": 4, "name": "Imagine Interiors"},
    {"id": 5, "name": "BD INTERIOR"}
]

# ✅ Hardcoded services
services = [
    {"company_id": 1, "name": "Bedroom", "price": 95000},
    {"company_id": 1, "name": "Kitchen", "price": 80000},
    {"company_id": 1, "name": "Living Room", "price": 100000},

    {"company_id": 2, "name": "Bedroom", "price": 115000},
    {"company_id": 2, "name": "Kitchen", "price": 88000},
    {"company_id": 2, "name": "Living Room", "price": 105000},

    {"company_id": 3, "name": "Bedroom", "price": 99000},
    {"company_id": 3, "name": "Kitchen", "price": 87000},
    {"company_id": 3, "name": "Living Room", "price": 93000},

    {"company_id": 4, "name": "Bedroom", "price": 105000},
    {"company_id": 4, "name": "Kitchen", "price": 89000},
    {"company_id": 4, "name": "Living Room", "price": 97000},

    {"company_id": 5, "name": "Bedroom", "price": 102000},
    {"company_id": 5, "name": "Kitchen", "price": 86000},
    {"company_id": 5, "name": "Living Room", "price": 95000}
]

@app.route('/')
def home():
    return render_template('index.html', companies=companies)

@app.route('/company/<int:company_id>')
def company_page(company_id):
    company = next(c for c in companies if c['id'] == company_id)
    service_list = [s for s in services if s['company_id'] == company_id]
    return render_template('company.html', company=company, services=service_list)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    selected_service = None
    results = []
    selected_ids = []

    if request.method == 'POST':
        # Get selected service (from compare or sort form)
        selected_service = request.form.get('service') or request.form.get('selected_service')
        selected_ids = request.form.getlist('companies')

        # Get selected sort method
        sort_order = request.form.get('sort')

        for company in companies:
            if str(company['id']) in selected_ids:
                service = next(
                    (s for s in services if s['company_id'] == company['id'] and s['name'] == selected_service),
                    None
                )
                if service:
                    results.append({
                        "company": company['name'],
                        "price": service['price']
                    })

        if sort_order == 'low_to_high':
            results.sort(key=lambda x: x['price'])
        elif sort_order == 'high_to_low':
            results.sort(key=lambda x: x['price'], reverse=True)

    return render_template(
        'compare.html',
        companies=companies,
        results=results,
        selected_service=selected_service,
        selected_ids=selected_ids
    )


if __name__ == '__main__':
    app.run(debug=True)
