package com.acorn.tour.sights;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.acorn.tour.paging.PageHandler;

	
@Component
public class SightsService {
	
	@Autowired
	SightsRepository rep;
	
	// 여행지
	// 조건에 맞는 전체 데이터 수
	public Integer getTotalCnt(int sidoCode) {
		int result = rep.totalCnt(sidoCode);
		return result;
	}
	
	// 최신순 content 10개씩 표출
	public ArrayList<SightDTO> getSelectAllLatest(int startList, int endList, int sidoCode) {
		ArrayList<SightDTO> list = (ArrayList<SightDTO>) rep.selectAllLatest(startList, endList, sidoCode);
		return list;
	}
	
	// 거리순 content 10개씩 표출
	public ArrayList<SightDTO> getSelectAllDistance(double lat1, double lon1, int startList, int endList, int sidoCode) {
		ArrayList<SightDTO> list = (ArrayList<SightDTO>) rep.getSelectAllDistance(lat1, lon1, startList, endList, sidoCode);
		ArrayList<SightDTO> distanceList= haversine(lat1, lon1, sidoCode);
		ArrayList<SightDTO> combinedList = new ArrayList<>();

		for (SightDTO listItem : list) {
		    for (SightDTO distanceItem : distanceList) {
		        if (listItem.getContentid().equals(distanceItem.getContentid())) {
		            combinedList.add(new SightDTO(
		                    listItem.getContentid(),
		                    listItem.getTitle(),
		                    listItem.getSidoCode(),
		                    listItem.getNickName(),
		                    listItem.getSigunguCode(),
		                    listItem.getSigunguname(),
		                    listItem.getFirstimage(),
		                    distanceItem.getDistance()
		            ));
		            break;
		        }
		    }
		}
		return combinedList;
	}
	
	// 인기순 content 10개씩 표출
	public ArrayList<SightDTO> getSelectAllPopular(int startList, int endList, int sidoCode){
		ArrayList<SightDTO> list = (ArrayList<SightDTO>) rep.getSelectAllPopular(startList, endList, sidoCode);
		return list;
	}
	
	// 상세페이지 해당 내용 
	public SightDTO getSelectOne(String contentId) {
		SightDTO content = rep.getSelectOne(contentId);
		return content;
	}
	
	// 페이징
	public PageHandler getPaging(int currentPage, int sidoCode) {
		
		int totRecords = getTotalCnt(sidoCode);
		int pageSize = 10;
		int grpSize = 10;
		
		PageHandler handler = new PageHandler(currentPage, totRecords, pageSize, grpSize);
		return handler;
	}
	// 위도 경도로 계산한 거리별로 정렬하기
	//public ArrayList<ContentDTO> haversine(double lat1, double lon1, int sidoCode,  String contenttypeid, String cat2) {
	public ArrayList<SightDTO> haversine(double lat1, double lon1, int sidoCode) {
		
		ArrayList<SightDTO> list = (ArrayList<SightDTO>) rep.distanceAll(sidoCode);
		ArrayList<SightDTO> listResult = new ArrayList<>();
        final int R = 6371; // 지구의 반지름 (단위: km)

        for(int i=0; i<list.size(); i++) {
        	// 위도와 경도를 라디안으로 변환
        	SightDTO item = list.get(i);
        	
            double lat1Rad = Math.toRadians(lat1); // 위도
            double lon1Rad = Math.toRadians(lon1); // 경도
            double lat2Rad = Math.toRadians(Double.parseDouble(item.getMapy()));
            double lon2Rad = Math.toRadians(Double.parseDouble(item.getMapx()));

            // Haversine 공식을 사용하여 거리 계산
            double dlat = lat2Rad - lat1Rad;
            double dlon = lon2Rad - lon1Rad;
            double a = Math.pow(Math.sin(dlat / 2), 2) + Math.cos(lat1Rad) * Math.cos(lat2Rad) * Math.pow(Math.sin(dlon / 2), 2);
            double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            double distance = R * c; // km
            
            listResult.add(new SightDTO(item.getContentid(), distance));
        }
        
        // 거리순으로 정렬
        Collections.sort(listResult, new Comparator<SightDTO>() {
			@Override
			public int compare(SightDTO o1, SightDTO o2) {
				return Double.compare(o1.getDistance(), o2.getDistance());
			}
        });

        return listResult;
    }
	
	
}
