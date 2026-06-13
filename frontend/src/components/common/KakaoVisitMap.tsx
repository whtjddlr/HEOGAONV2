"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { loadKakaoMap } from "@/lib/kakaoMap";
import type { VisitLocation } from "@/types/flow";

const DEFAULT_CENTER: VisitLocation = { lat: 37.5665, lng: 126.9018 };

export function KakaoVisitMap({
  keyword,
  defaultLocation,
  directionUrl,
  selectedLocation,
  onSelect,
}: {
  keyword: string;
  defaultLocation: VisitLocation | null;
  directionUrl?: string;
  selectedLocation: VisitLocation | null;
  onSelect: (location: VisitLocation) => void;
}) {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<any>(null);
  const markerRef = useRef<any>(null);
  const onSelectRef = useRef(onSelect);
  const [status, setStatus] = useState("지도를 불러오는 중이에요.");

  useEffect(() => {
    onSelectRef.current = onSelect;
  }, [onSelect]);

  const updateMarker = useCallback((lat: number, lng: number, address?: string) => {
    const kakao = window.kakao;
    const position = new kakao.maps.LatLng(lat, lng);
    mapInstanceRef.current?.setCenter(position);
    markerRef.current?.setPosition(position);
    onSelectRef.current({ lat, lng, address });
    setStatus(address || "선택한 위치를 저장했어요.");
  }, []);

  useEffect(() => {
    let mounted = true;

    loadKakaoMap()
      .then(() => {
        if (!mounted || !mapRef.current) return;

        const kakao = window.kakao;
        const initial = selectedLocation || defaultLocation || DEFAULT_CENTER;
        const center = new kakao.maps.LatLng(initial.lat, initial.lng);
        const map = new kakao.maps.Map(mapRef.current, {
          center,
          level: 4,
        });
        const marker = new kakao.maps.Marker({ position: center, map });
        const geocoder = new kakao.maps.services.Geocoder();
        const places = new kakao.maps.services.Places();

        mapInstanceRef.current = map;
        markerRef.current = marker;

        if (selectedLocation || defaultLocation) {
          setStatus(initial.address || "방문 위치를 지도에 표시했어요.");
        } else {
          places.keywordSearch(keyword, (result: any[], searchStatus: string) => {
            if (!mounted) return;
            if (searchStatus === kakao.maps.services.Status.OK && result[0]) {
              updateMarker(Number(result[0].y), Number(result[0].x), result[0].address_name || result[0].road_address_name);
              return;
            }
            setStatus("지도에서 방문 위치를 눌러주세요.");
          });
        }

        kakao.maps.event.addListener(map, "click", (mouseEvent: any) => {
          const latlng = mouseEvent.latLng;
          marker.setPosition(latlng);

          geocoder.coord2Address(latlng.getLng(), latlng.getLat(), (result: any[], geoStatus: string) => {
            const address =
              geoStatus === kakao.maps.services.Status.OK
                ? result[0]?.road_address?.address_name || result[0]?.address?.address_name
                : "";
            updateMarker(latlng.getLat(), latlng.getLng(), address);
          });
        });
      })
      .catch((error) => {
        if (mounted) {
          const message = error instanceof Error ? error.message : "";
          setStatus(
            message === "KAKAO_MAP_API_KEY_MISSING"
              ? "지도 키를 읽지 못했어요. 프론트 서버를 재시작해주세요."
              : "카카오 지도 SDK를 불러오지 못했어요. 도메인 설정과 네트워크를 확인해주세요."
          );
        }
      });

    return () => {
      mounted = false;
    };
  }, [defaultLocation, keyword, selectedLocation, updateMarker]);

  return (
    <div className="visit-map-block">
      <div ref={mapRef} className="visit-map" role="application" aria-label="방문 위치 선택 지도" />
      <div className="visit-map-status-row">
        <p className="visit-map-status" role="status" aria-live="polite">{status}</p>
        {directionUrl ? (
          <a
            className="visit-map-direction"
            href={directionUrl}
            target="_blank"
            rel="noreferrer"
            aria-label="카카오맵 길찾기"
          >
            길찾기
          </a>
        ) : null}
      </div>
    </div>
  );
}
