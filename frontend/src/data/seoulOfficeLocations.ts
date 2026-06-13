import type { VisitLocation } from "@/types/flow";

export interface SeoulOfficeLocation extends VisitLocation {
  districtName: string;
  officeName: string;
  officeAddress: string;
}

export const SEOUL_OFFICE_LOCATIONS: SeoulOfficeLocation[] = [
  { districtName: "종로구", officeName: "종로구청", officeAddress: "서울특별시 종로구 삼봉로 43", lat: 37.5723031, lng: 126.9808398, address: "서울특별시 종로구 삼봉로 43" },
  { districtName: "중구", officeName: "중구청", officeAddress: "서울특별시 중구 창경궁로 17", lat: 37.563758, lng: 126.9975659, address: "서울특별시 중구 창경궁로 17" },
  { districtName: "용산구", officeName: "용산구청", officeAddress: "서울특별시 용산구 녹사평대로 150", lat: 37.5325763, lng: 126.9904206, address: "서울특별시 용산구 녹사평대로 150" },
  { districtName: "성동구", officeName: "성동구청", officeAddress: "서울특별시 성동구 고산자로 270", lat: 37.5634661, lng: 127.0368984, address: "서울특별시 성동구 고산자로 270" },
  { districtName: "광진구", officeName: "광진구청", officeAddress: "서울특별시 광진구 자양로 117", lat: 37.5384976, lng: 127.0819157, address: "서울특별시 광진구 자양로 117" },
  { districtName: "동대문구", officeName: "동대문구청", officeAddress: "서울특별시 동대문구 천호대로 145", lat: 37.574524, lng: 127.03965, address: "서울특별시 동대문구 천호대로 145" },
  { districtName: "중랑구", officeName: "중랑구청", officeAddress: "서울특별시 중랑구 봉화산로 179", lat: 37.6063242, lng: 127.0925842, address: "서울특별시 중랑구 봉화산로 179" },
  { districtName: "성북구", officeName: "성북구청", officeAddress: "서울특별시 성북구 보문로 168", lat: 37.5894684, lng: 127.0168275, address: "서울특별시 성북구 보문로 168" },
  { districtName: "강북구", officeName: "강북구청", officeAddress: "서울특별시 강북구 도봉로89길 13", lat: 37.6397199, lng: 127.0256882, address: "서울특별시 강북구 도봉로89길 13" },
  { districtName: "도봉구", officeName: "도봉구청", officeAddress: "서울특별시 도봉구 마들로 656", lat: 37.6687201, lng: 127.0473035, address: "서울특별시 도봉구 마들로 656" },
  { districtName: "노원구", officeName: "노원구청", officeAddress: "서울특별시 노원구 노해로 437", lat: 37.6543998, lng: 127.056431, address: "서울특별시 노원구 노해로 437" },
  { districtName: "은평구", officeName: "은평구청", officeAddress: "서울특별시 은평구 은평로 195", lat: 37.6024668, lng: 126.9288202, address: "서울특별시 은평구 은평로 195" },
  { districtName: "서대문구", officeName: "서대문구청", officeAddress: "서울특별시 서대문구 연희로 248", lat: 37.579182, lng: 126.9367984, address: "서울특별시 서대문구 연희로 248" },
  { districtName: "마포구", officeName: "마포구청", officeAddress: "서울특별시 마포구 월드컵로 212", lat: 37.5663245, lng: 126.901491, address: "서울특별시 마포구 월드컵로 212" },
  { districtName: "양천구", officeName: "양천구청", officeAddress: "서울특별시 양천구 목동동로 105", lat: 37.5168721, lng: 126.8663985, address: "서울특별시 양천구 목동동로 105" },
  { districtName: "강서구", officeName: "강서구청", officeAddress: "서울특별시 강서구 화곡로 302", lat: 37.550659, lng: 126.84977, address: "서울특별시 강서구 화곡로 302" },
  { districtName: "구로구", officeName: "구로구청", officeAddress: "서울특별시 구로구 가마산로 245", lat: 37.4955112, lng: 126.8882948, address: "서울특별시 구로구 가마산로 245" },
  { districtName: "금천구", officeName: "금천구청", officeAddress: "서울특별시 금천구 시흥대로73길 70", lat: 37.4568996, lng: 126.8953809, address: "서울특별시 금천구 시흥대로73길 70" },
  { districtName: "영등포구", officeName: "영등포구청", officeAddress: "서울특별시 영등포구 당산로 123", lat: 37.5264807, lng: 126.8956526, address: "서울특별시 영등포구 당산로 123" },
  { districtName: "동작구", officeName: "동작구청", officeAddress: "서울특별시 동작구 장승배기로 161", lat: 37.5125292, lng: 126.9399439, address: "서울특별시 동작구 장승배기로 161" },
  { districtName: "관악구", officeName: "관악구청", officeAddress: "서울특별시 관악구 관악로 145", lat: 37.4784684, lng: 126.9511015, address: "서울특별시 관악구 관악로 145" },
  { districtName: "서초구", officeName: "서초구청", officeAddress: "서울특별시 서초구 남부순환로 2584", lat: 37.4835926, lng: 127.0334589, address: "서울특별시 서초구 남부순환로 2584" },
  { districtName: "강남구", officeName: "강남구청", officeAddress: "서울특별시 강남구 학동로 426", lat: 37.5172363, lng: 127.0473248, address: "서울특별시 강남구 학동로 426" },
  { districtName: "송파구", officeName: "송파구청", officeAddress: "서울특별시 송파구 올림픽로 326", lat: 37.5145656, lng: 127.1060321, address: "서울특별시 송파구 올림픽로 326" },
  { districtName: "강동구", officeName: "강동구청", officeAddress: "서울특별시 강동구 성내로 25", lat: 37.530126, lng: 127.12377, address: "서울특별시 강동구 성내로 25" },
];

export function findSeoulOfficeLocation(text: string) {
  return SEOUL_OFFICE_LOCATIONS.find((location) => text.includes(location.districtName)) || null;
}

export function kakaoDirectionUrl(location: SeoulOfficeLocation) {
  const label = encodeURIComponent(location.officeName);
  return `https://map.kakao.com/link/to/${label},${location.lat},${location.lng}`;
}
