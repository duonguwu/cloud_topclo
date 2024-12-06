from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Endpoint giả lập từ nơi cung cấp sản phẩm
PRODUCTS_API_URL = "https://cloudclothes.azurewebsites.net/products"  # Thay đổi URL theo endpoint thực tế

@app.route('/top-discount-products', methods=['GET'])
def get_top_discount_products():
    try:
        # Lấy dữ liệu từ API
        response = requests.get(PRODUCTS_API_URL)
        response.raise_for_status()
        products_data = response.json()

        # Lọc sản phẩm có oldPrice
        discounted_products = []
        for product in products_data.get('products', []):
            if 'oldPrice' in product and product['oldPrice'] > product['price']:
                discount = product['oldPrice'] - product['price']
                product['discount'] = discount
                discounted_products.append(product)

        # Sắp xếp sản phẩm theo mức giảm giá từ cao đến thấp
        discounted_products.sort(key=lambda x: x['discount'], reverse=True)

        # Lấy 3 sản phẩm có mức giảm giá cao nhất
        top_3_products = discounted_products[:3]

        # Trả về dữ liệu JSON
        return jsonify(top_3_products), 200

    except requests.exceptions.RequestException as e:
        # Nếu có lỗi khi gọi API
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
