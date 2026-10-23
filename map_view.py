"""정제 CSV의 df를 받아 카카오 지도 HTML 문자열을 만든다. (JavaScript 키만 사용)"""
import html
import json

MAX_MARKERS = 200


def kakao_map_html(js_key, df, height=500):
    """df(이름·주소·위도·경도·개방시간 컬럼)로 마커가 찍힌 지도 HTML을 돌려준다.

    마커는 최대 200개, 클릭하면 이름·개방시간이 뜬다. 빈 df면 서울 시청 중심의 빈 지도.
    """
    rows = df.head(MAX_MARKERS)
    markers = [
        {
            "lat": float(r["위도"]),
            "lng": float(r["경도"]),
            "name": html.escape(str(r["이름"])),
            "hours": html.escape(str(r["개방시간"])),
        }
        for _, r in rows.iterrows()
    ]
    center = (
        (rows["위도"].astype(float).mean(), rows["경도"].astype(float).mean())
        if markers
        else (37.5665, 126.9780)
    )
    # "</" 이스케이프: 데이터 안에 </script> 가 있어도 스크립트가 끊기지 않게
    data = json.dumps(markers, ensure_ascii=False).replace("</", "<\\/")
    return f"""<div id="map" style="width:100%;height:{int(height)}px;"></div>
<script src="//dapi.kakao.com/v2/maps/sdk.js?appkey={html.escape(str(js_key))}"></script>
<script>
  var markers = {data};
  var map = new kakao.maps.Map(document.getElementById("map"), {{
    center: new kakao.maps.LatLng({center[0]}, {center[1]}),
    level: 5
  }});
  var info = new kakao.maps.InfoWindow({{ removable: true }});
  markers.forEach(function (m) {{
    var marker = new kakao.maps.Marker({{
      map: map,
      position: new kakao.maps.LatLng(m.lat, m.lng)  // LatLng(위도, 경도) 순서
    }});
    kakao.maps.event.addListener(marker, "click", function () {{
      info.setContent('<div style="padding:8px;font-size:12px;">' +
        '<b>' + m.name + '</b><br>개방시간: ' + m.hours + '</div>');
      info.open(map, marker);
    }});
  }});
</script>"""
