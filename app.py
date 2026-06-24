from flask import Flask, jsonify, abort
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Data Source: Mapping of selected Kenyan Counties to their Sub-counties
# Note: This is a representative dataset for the API structure.
KENYA_DATA = {
    "Baringo": ["Baringo Central", "Baringo North", "Baringo South", "Eldama Ravine", "Mogotio", "Tiaty"],
    "Bomet": ["Bomet Central", "Bomet East", "Chepalungu", "Konoin", "Sotik"],
    "Bungoma": ["Bumula", "Kabuchai", "Kanduyi", "Kimilili", "Mt Elgon", "Sirisia", "Tongaren", "Webuye East", "Webuye West"],
    "Busia": ["Butula", "Funyula", "Matayos", "Nambale", "Teso North", "Teso South"],
    "Elgeyo Marakwet": ["Keiyo North", "Keiyo South", "Marakwet East", "Marakwet West"],
    "Embu": ["Manyatta", "Mbeere North", "Mbeere South", "Runyenjes"],
    "Garissa": ["Dadaab", "Fafi", "Garissa Township", "Hulugho", "Ijara", "Lagdera"],
    "Homa Bay": ["Homa Bay Town", "Kabondo Kasipul", "Kasipul", "Mbita", "Ndhiwa", "Rangwe", "Suba North", "Suba South"],
    "Isiolo": ["Isiolo", "Garbatulla", "Merti"],
    "Kajiado": ["Kajiado Central", "Kajiado East", "Kajiado North", "Kajiado West", "Loitokitok"],
    "Kakamega": ["Butere", "Khwisero", "Likuyani", "Lugari", "Lurambi", "Matungu", "Mumias East", "Mumias West", "Navakholo", "Shinyalu", "Ikolomani"],
    "Kericho": ["Ainamoi", "Belgut", "Bureti", "Kipkelion East", "Kipkelion West", "Sigowet-Soin"],
    "Kiambu": ["Gatundu North", "Gatundu South", "Githunguri", "Juja", "Kabete", "Kiambaa", "Kiambu", "Kikuyu", "Lari", "Limuru", "Ruiru", "Thika Town"],
    "Kilifi": ["Ganze", "Kaloleni", "Kilifi North", "Kilifi South", "Magarini", "Malindi", "Rabai"],
    "Kirinyaga": ["Gichugu", "Kirinyaga Central", "Kirinyaga East", "Kirinyaga West", "Mwea"],
    "Kisii": ["Bobasi", "Bomachoge Borabu", "Bomachoge Chache", "Bonchari", "South Mugirango", "Kitutu Chache North", "Kitutu Chache South", "Nyaribari Chache", "Nyaribari Masaba"],
    "Kisumu": ["Kisumu Central", "Kisumu East", "Kisumu West", "Muhoroni", "Nyakach", "Nyando", "Seme"],
    "Mombasa": ["Changamwe", "Jomvu", "Kisauni", "Likoni", "Mvita", "Nyali"],
    "Nairobi": ["Dagoretti North", "Dagoretti South", "Embakasi Central", "Embakasi East", "Embakasi North", "Embakasi South", "Embakasi West", "Kamukunji", "Kasarani", "Kibra", "Lang'ata", "Makadara", "Mathare", "Roysambu", "Ruaraka", "Starehe", "Westlands"],
    "Nakuru": ["Bahati", "Gilgil", "Kuresoi North", "Kuresoi South", "Molo", "Naivasha", "Nakuru City East", "Nakuru City West", "Njoro", "Rongai", "Subukia"]
}

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({"status": "active", "version": "1.0.0", "timestamp": "2026-06-24"})

@app.route('/api/v1/counties', methods=['GET'])
def get_counties():
    """Returns a list of all available county names."""
    counties = sorted(list(KENYA_DATA.keys()))
    return jsonify({
        "count": len(counties),
        "counties": counties
    })

@app.route('/api/v1/counties/<string:county_name>', methods=['GET'])
def get_county_details(county_name):
    """Returns sub-counties for a specific county (case-insensitive)."""
    lookup = {k.lower(): k for k in KENYA_DATA.keys()}
    normalized_name = county_name.lower()
    
    if normalized_name not in lookup:
        abort(404, description=f"County '{county_name}' not found.")
        
    actual_name = lookup[normalized_name]
    return jsonify({
        "county": actual_name,
        "sub_counties": KENYA_DATA[actual_name],
        "total_sub_counties": len(KENYA_DATA[actual_name])
    })

@app.route('/api/v1/search/subcounties/<string:query>', methods=['GET'])
def search_subcounties(query):
    """Search for sub-counties matching a query string."""
    results = []
    q = query.lower()
    for county, subs in KENYA_DATA.items():
        for s in subs:
            if q in s.lower():
                results.append({"sub_county": s, "county": county})
    return jsonify({"query": query, "results": results, "count": len(results)})

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))