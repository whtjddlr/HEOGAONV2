let kakaoMapPromise: Promise<void> | null = null;

export function loadKakaoMap() {
  if (typeof window === "undefined") {
    return Promise.reject(new Error("Kakao map can only load in browser."));
  }

  if (window.kakao?.maps) {
    return Promise.resolve();
  }

  if (kakaoMapPromise) {
    return kakaoMapPromise;
  }

  const appKey = process.env.NEXT_PUBLIC_KAKAO_MAP_API_KEY;
  if (!appKey) {
    return Promise.reject(new Error("KAKAO_MAP_API_KEY_MISSING"));
  }

  kakaoMapPromise = new Promise((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>("script[data-kakao-map-sdk='true']");
    if (existing) {
      existing.addEventListener("load", () => window.kakao.maps.load(() => resolve()), { once: true });
      existing.addEventListener("error", () => reject(new Error("KAKAO_MAP_SDK_LOAD_FAILED")), { once: true });
      return;
    }

    const script = document.createElement("script");
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${appKey}&autoload=false&libraries=services`;
    script.async = true;
    script.dataset.kakaoMapSdk = "true";
    script.onload = () => window.kakao.maps.load(() => resolve());
    script.onerror = () => reject(new Error("KAKAO_MAP_SDK_LOAD_FAILED"));
    document.head.appendChild(script);
  });

  return kakaoMapPromise;
}
