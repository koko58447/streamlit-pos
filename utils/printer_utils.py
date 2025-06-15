from escpos.printer import Usb
from PIL import Image

total=0

def print_invoice(customer_name, phone, items):

    """
    customer_name: ဖောက်သည်နာမည်
    phone: ဖုန်းနံပါတ်
    items: item list (name, qty, price)
    """
    try:
        p = Usb(0x04B8, 0x0E15, 0)  # Printer Vendor ID & Product ID ပြင်ပါ

        p.set(align="center")
        p.text("My Shop\n")
        p.text("No.123, Yangon\n")
        p.text("Phone: 09-123456789\n")
        p.text("----------------------------\n")

        p.set(align="left")
        p.text(f"Customer: {customer_name}\n")
        p.text(f"Phone: {phone}\n")
        p.text("----------------------------\n")

        total = 0
        p.text("Item\tQty\tPrice\n")
        for name, qty, price in items:
            p.text(f"{name}\t{qty}\t{price:.2f}\n")
            total += qty * price

        p.text("----------------------------\n")
        p.set(align="right")
        p.text(f"Total: {total:.2f} MMK\n")
        p.text("Thank you for your purchase!\n")
        p.cut()

        return True
    except Exception as e:
        print("Print Error:", e)
        return False
    
def render_voucher(customer_name, phone, items):
    html = f"""

     <style>
        .voucher {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            max-width: 600px;
            margin: auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            font-family: 'Myanmar3', 'Pyidaungsu', sans-serif;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .customer-info {{
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        tfoot td {{
            font-weight: bold;
            background-color: #f5f5f5;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #555;
        }}
        .print-btn {{
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .print-btn:hover {{
            background-color: #0b5ed7;
        }}
    </style>
    
    <div style="font-family: sans-serif; max-width: 400px; margin: auto;">
        <h3>🧾 Voucher</h3>
        <p><b>Customer:</b> {customer_name}</p>
        <p><b>Phone:</b> {phone}</p>
        <table style="width:100%; border-collapse: collapse;">
            <tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>
    """

    for item in items:
        qty = float(item["qty"])
        price = float(item["price"])
        line_total = qty * price
        html += f"""
        <tr>
            <td>{item['name']}</td>
            <td>{qty}</td>
            <td>{price:.2f}</td>
            <td>{line_total:.2f}</td>
        </tr>
        """

    total = sum(float(item["qty"]) * float(item["price"]) for item in items)

    html += f"""
        <tr><td colspan="3" style="text-align:right;"><b>Grand Total</b></td><td><b>{total:.2f}</b></td></tr>
        </table>
        <p style="text-align:center;">Thank you for shopping!</p>
    </div>
    """
    return html

def render_voucher1(customer_name, phone, items):
    """
    Voucher ကို HTML + CSS နဲ့ render
    """
    total = sum(float(item["qty"]) * float(item["price"]) for item in items)

    html = f"""
    <style>
        .voucher {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            max-width: 600px;
            margin: auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            font-family: 'Myanmar3', 'Pyidaungsu', sans-serif;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .customer-info {{
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        tfoot td {{
            font-weight: bold;
            background-color: #f5f5f5;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #555;
        }}
        .print-btn {{
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .print-btn:hover {{
            background-color: #0b5ed7;
        }}
    </style>

    <div class="voucher">
        <div class="header">
            <h2>My Shop</h2>
            <p>No.123, Yangon</p>
            <p>Phone: 09-123456789</p>
        </div>

        <div class="customer-info">
            <p><strong>Customer:</strong> {customer_name}</p>
            <p><strong>Phone:</strong> {phone}</p>
        </div>

        <table>
            <thead>
                <tr>
                    <th>code</th>
                    <th>Item</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
    """

    for code,name, qty, price in items:
        item_total = qty * price
        html += f"""
        <tr>
            <td>{code}</td>
            <td>{name}</td>
            <td>{qty}</td>
            <td>{price:.2f} MMK</td>
            <td>{item_total:.2f} MMK</td>
        </tr>
        """

    html += f"""
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="4" style="text-align:right;">Total:</td>
                    <td>{total:.2f} MMK</td>
                </tr>
            </tfoot>
        </table>

        <div class="footer">
            <p>ဝယ်ယူတဲ့အတွက်ကျေးဇူးတင်ပါတယ်။</p>
        </div>

        <button class="print-btn" onclick="window.print()">🖨️ Print Voucher</button>
    </div>
    """

    return html
