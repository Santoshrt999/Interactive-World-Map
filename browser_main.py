import http.server
import socketserver
import webbrowser
import os
import json
import urllib.parse

PORT = 8000
BASE_DIR = os.path.join(os.path.dirname(__file__), "web")

COUNTRY_STATS = {
    'AFG':{'name':'Afghanistan','population':41,'gdp':14,'climate':12,'internet':18},
    'AGO':{'name':'Angola','population':34,'gdp':106,'climate':22,'internet':33},
    'ARG':{'name':'Argentina','population':46,'gdp':640,'climate':16,'internet':82},
    'AUS':{'name':'Australia','population':26,'gdp':1723,'climate':22,'internet':96},
    'AUT':{'name':'Austria','population':9,'gdp':526,'climate':9,'internet':93},
    'AZE':{'name':'Azerbaijan','population':10,'gdp':78,'climate':15,'internet':84},
    'BEL':{'name':'Belgium','population':11,'gdp':627,'climate':11,'internet':92},
    'BEN':{'name':'Benin','population':13,'gdp':20,'climate':28,'internet':26},
    'BFA':{'name':'Burkina Faso','population':22,'gdp':20,'climate':29,'internet':22},
    'BGD':{'name':'Bangladesh','population':170,'gdp':457,'climate':26,'internet':39},
    'BHR':{'name':'Bahrain','population':2,'gdp':46,'climate':28,'internet':99},
    'BLR':{'name':'Belarus','population':10,'gdp':74,'climate':8,'internet':89},
    'BOL':{'name':'Bolivia','population':12,'gdp':46,'climate':18,'internet':48},
    'BRA':{'name':'Brazil','population':215,'gdp':2331,'climate':25,'internet':81},
    'BGR':{'name':'Bulgaria','population':7,'gdp':101,'climate':12,'internet':84},
    'CAN':{'name':'Canada','population':38,'gdp':2242,'climate':0,'internet':94},
    'CHE':{'name':'Switzerland','population':9,'gdp':905,'climate':9,'internet':97},
    'CHL':{'name':'Chile','population':19,'gdp':336,'climate':12,'internet':88},
    'CHN':{'name':'China','population':1412,'gdp':18530,'climate':14,'internet':73},
    'CIV':{'name':'Ivory Coast','population':26,'gdp':79,'climate':27,'internet':43},
    'CMR':{'name':'Cameroon','population':27,'gdp':48,'climate':25,'internet':37},
    'COD':{'name':'DR Congo','population':100,'gdp':67,'climate':24,'internet':18},
    'COL':{'name':'Colombia','population':51,'gdp':363,'climate':24,'internet':73},
    'CUB':{'name':'Cuba','population':11,'gdp':107,'climate':26,'internet':62},
    'CZE':{'name':'Czech Republic','population':11,'gdp':336,'climate':9,'internet':91},
    'DEU':{'name':'Germany','population':84,'gdp':4456,'climate':10,'internet':92},
    'DZA':{'name':'Algeria','population':45,'gdp':239,'climate':12,'internet':63},
    'DNK':{'name':'Denmark','population':6,'gdp':430,'climate':9,'internet':99},
    'ECU':{'name':'Ecuador','population':18,'gdp':122,'climate':22,'internet':67},
    'EGY':{'name':'Egypt','population':105,'gdp':358,'climate':22,'internet':72},
    'ESP':{'name':'Spain','population':47,'gdp':1581,'climate':16,'internet':93},
    'EST':{'name':'Estonia','population':1,'gdp':43,'climate':7,'internet':94},
    'ETH':{'name':'Ethiopia','population':123,'gdp':163,'climate':22,'internet':24},
    'FIN':{'name':'Finland','population':6,'gdp':305,'climate':4,'internet':97},
    'FJI':{'name':'Fiji','population':1,'gdp':5,'climate':26,'internet':59},
    'FRA':{'name':'France','population':68,'gdp':3130,'climate':13,'internet':93},
    'GBR':{'name':'United Kingdom','population':67,'gdp':3340,'climate':11,'internet':96},
    'GHA':{'name':'Ghana','population':32,'gdp':76,'climate':27,'internet':58},
    'GIN':{'name':'Guinea','population':13,'gdp':18,'climate':27,'internet':23},
    'GRC':{'name':'Greece','population':11,'gdp':242,'climate':18,'internet':84},
    'GTM':{'name':'Guatemala','population':17,'gdp':98,'climate':24,'internet':55},
    'HKG':{'name':'Hong Kong','population':7,'gdp':383,'climate':24,'internet':95},
    'HND':{'name':'Honduras','population':10,'gdp':35,'climate':25,'internet':43},
    'HRV':{'name':'Croatia','population':4,'gdp':82,'climate':13,'internet':90},
    'HTI':{'name':'Haiti','population':12,'gdp':19,'climate':28,'internet':33},
    'HUN':{'name':'Hungary','population':10,'gdp':212,'climate':11,'internet':91},
    'IDN':{'name':'Indonesia','population':277,'gdp':1476,'climate':27,'internet':66},
    'IND':{'name':'India','population':1408,'gdp':4110,'climate':25,'internet':52},
    'IRN':{'name':'Iran','population':86,'gdp':401,'climate':18,'internet':78},
    'IRQ':{'name':'Iraq','population':42,'gdp':268,'climate':23,'internet':71},
    'ISR':{'name':'Israel','population':9,'gdp':509,'climate':21,'internet':90},
    'ITA':{'name':'Italy','population':60,'gdp':2172,'climate':15,'internet':88},
    'JOR':{'name':'Jordan','population':10,'gdp':51,'climate':18,'internet':85},
    'JPN':{'name':'Japan','population':125,'gdp':4110,'climate':16,'internet':93},
    'KAZ':{'name':'Kazakhstan','population':19,'gdp':261,'climate':8,'internet':88},
    'KEN':{'name':'Kenya','population':55,'gdp':118,'climate':22,'internet':42},
    'KOR':{'name':'South Korea','population':52,'gdp':1760,'climate':13,'internet':97},
    'KWT':{'name':'Kuwait','population':4,'gdp':163,'climate':28,'internet':99},
    'LBN':{'name':'Lebanon','population':5,'gdp':25,'climate':20,'internet':84},
    'LBY':{'name':'Libya','population':7,'gdp':46,'climate':20,'internet':62},
    'LKA':{'name':'Sri Lanka','population':22,'gdp':87,'climate':28,'internet':44},
    'LTU':{'name':'Lithuania','population':3,'gdp':82,'climate':8,'internet':90},
    'LVA':{'name':'Latvia','population':2,'gdp':47,'climate':7,'internet':91},
    'MAR':{'name':'Morocco','population':37,'gdp':160,'climate':18,'internet':88},
    'MDG':{'name':'Madagascar','population':28,'gdp':16,'climate':22,'internet':20},
    'MEX':{'name':'Mexico','population':128,'gdp':1789,'climate':21,'internet':76},
    'MLI':{'name':'Mali','population':22,'gdp':22,'climate':29,'internet':24},
    'MMR':{'name':'Myanmar','population':55,'gdp':68,'climate':27,'internet':38},
    'MNG':{'name':'Mongolia','population':3,'gdp':22,'climate':1,'internet':76},
    'MOZ':{'name':'Mozambique','population':32,'gdp':20,'climate':23,'internet':17},
    'MYS':{'name':'Malaysia','population':33,'gdp':438,'climate':27,'internet':91},
    'MWI':{'name':'Malawi','population':20,'gdp':14,'climate':23,'internet':18},
    'NER':{'name':'Niger','population':25,'gdp':17,'climate':29,'internet':14},
    'NGA':{'name':'Nigeria','population':218,'gdp':506,'climate':28,'internet':36},
    'NLD':{'name':'Netherlands','population':18,'gdp':1118,'climate':11,'internet':97},
    'NOR':{'name':'Norway','population':5,'gdp':593,'climate':4,'internet':99},
    'NZL':{'name':'New Zealand','population':5,'gdp':253,'climate':14,'internet':96},
    'OMN':{'name':'Oman','population':5,'gdp':108,'climate':28,'internet':90},
    'PAK':{'name':'Pakistan','population':231,'gdp':374,'climate':22,'internet':36},
    'PER':{'name':'Peru','population':33,'gdp':268,'climate':19,'internet':71},
    'PHL':{'name':'Philippines','population':115,'gdp':468,'climate':27,'internet':68},
    'PNG':{'name':'Papua New Guinea','population':10,'gdp':33,'climate':26,'internet':15},
    'POL':{'name':'Poland','population':38,'gdp':811,'climate':9,'internet':91},
    'PRT':{'name':'Portugal','population':10,'gdp':287,'climate':17,'internet':88},
    'PRY':{'name':'Paraguay','population':7,'gdp':44,'climate':24,'internet':66},
    'QAT':{'name':'Qatar','population':3,'gdp':213,'climate':29,'internet':99},
    'ROU':{'name':'Romania','population':19,'gdp':351,'climate':10,'internet':87},
    'RUS':{'name':'Russia','population':144,'gdp':2021,'climate':0,'internet':88},
    'RWA':{'name':'Rwanda','population':14,'gdp':14,'climate':21,'internet':30},
    'SAU':{'name':'Saudi Arabia','population':36,'gdp':1103,'climate':26,'internet':98},
    'SDN':{'name':'Sudan','population':45,'gdp':33,'climate':25,'internet':31},
    'SEN':{'name':'Senegal','population':17,'gdp':31,'climate':28,'internet':53},
    'SGP':{'name':'Singapore','population':6,'gdp':501,'climate':28,'internet':97},
    'SOM':{'name':'Somalia','population':17,'gdp':11,'climate':28,'internet':12},
    'SRB':{'name':'Serbia','population':7,'gdp':75,'climate':12,'internet':83},
    'SVK':{'name':'Slovakia','population':6,'gdp':135,'climate':10,'internet':90},
    'SVN':{'name':'Slovenia','population':2,'gdp':70,'climate':11,'internet':90},
    'SWE':{'name':'Sweden','population':10,'gdp':597,'climate':6,'internet':97},
    'SYR':{'name':'Syria','population':21,'gdp':25,'climate':18,'internet':42},
    'TCD':{'name':'Chad','population':17,'gdp':13,'climate':27,'internet':11},
    'THA':{'name':'Thailand','population':72,'gdp':544,'climate':28,'internet':72},
    'TJK':{'name':'Tajikistan','population':10,'gdp':12,'climate':11,'internet':34},
    'TUN':{'name':'Tunisia','population':12,'gdp':48,'climate':19,'internet':74},
    'TUR':{'name':'Turkey','population':85,'gdp':1344,'climate':14,'internet':81},
    'TWN':{'name':'Taiwan','population':23,'gdp':807,'climate':24,'internet':92},
    'TZA':{'name':'Tanzania','population':64,'gdp':83,'climate':23,'internet':26},
    'UGA':{'name':'Uganda','population':47,'gdp':50,'climate':23,'internet':26},
    'UKR':{'name':'Ukraine','population':44,'gdp':175,'climate':9,'internet':79},
    'ARE':{'name':'UAE','population':10,'gdp':527,'climate':28,'internet':99},
    'USA':{'name':'United States','population':335,'gdp':28780,'climate':12,'internet':92},
    'VEN':{'name':'Venezuela','population':29,'gdp':92,'climate':28,'internet':72},
    'VNM':{'name':'Vietnam','population':97,'gdp':469,'climate':27,'internet':74},
    'ZAF':{'name':'South Africa','population':60,'gdp':373,'climate':17,'internet':72},
    'ZMB':{'name':'Zambia','population':19,'gdp':29,'climate':20,'internet':26},
    'ZWE':{'name':'Zimbabwe','population':16,'gdp':26,'climate':21,'internet':34},
}


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/insight'):
            self._handle_insight()
            return
        super().do_GET()

    def _handle_insight(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        iso3 = params.get('country', [None])[0]
        try:
            import anthropic
            stats = COUNTRY_STATS.get(iso3, {})
            name = stats.get('name', iso3 or 'Unknown')
            client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''))
            msg = client.messages.create(
                model='claude-sonnet-4-6',
                max_tokens=300,
                messages=[{
                    'role': 'user',
                    'content': (
                        f"You are a geopolitical and economic analyst. Given that {name} "
                        f"has these stats: GDP=${stats.get('gdp','N/A')}B, "
                        f"Population={stats.get('population','N/A')}M, "
                        f"Climate={stats.get('climate','N/A')}°C avg, "
                        f"Internet Penetration={stats.get('internet','N/A')}%, "
                        f"provide a 3-sentence insight about its development trajectory, "
                        f"key challenges, and one opportunity. Be factual and neutral."
                    )
                }]
            )
            self._json(200, {'insight': msg.content[0].text, 'country': name})
        except ImportError:
            self._json(503, {'error': 'Run: pip install anthropic'})
        except Exception as e:
            msg = str(e)
            if 'api_key' in msg.lower() or 'authentication' in msg.lower() or 'auth_token' in msg.lower():
                self._json(401, {'error': 'Set the ANTHROPIC_API_KEY environment variable to use AI Insight.'})
            else:
                self._json(500, {'error': msg})

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def run(port: int = PORT) -> int:
    os.chdir(BASE_DIR)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), Handler) as httpd:
        url = f"http://127.0.0.1:{port}"
        print(f"Serving Interactive World Map at {url}")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
