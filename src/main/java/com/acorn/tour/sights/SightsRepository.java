package com.acorn.tour.sights;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;



@Component
public class SightsRepository {
	

	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.SightsMapper.";
	
	// 여행지
	// 조건에 맞는 전체 데이터 수
	public Integer totalCnt(int sidoCode) {
		int result = session.selectOne(namespace+"totalCnt",sidoCode);
		return result;
	}
	
	// 최신순 content 10개씩 표출
	public List<SightDTO> selectAllLatest(int startList, int endList, int sidoCode) {
		Map<String, Object> params = new HashMap<>();
		params.put("startList", startList);
	    params.put("endList", endList);
	    params.put("sidoCode", sidoCode);
		return session.selectList(namespace+"selectAllLatest",params);
	}
	public List<SightDTO> distanceAll(int sidoCode){
		return session.selectOne(namespace +" distanceAll",sidoCode);
	}
	// 거리순 content 10개씩 표출
	public List<SightDTO> getSelectAllDistance(double lat1, double lon1, int startList, int endList, int sidoCode) {
		return session.selectList(namespace+"selectAllDistance",sidoCode);
	}
	
	// 인기순 content 10개씩 표출
	public List<SightDTO> getSelectAllPopular(int startList, int endList, int sidoCode){
		Map<String, Object> params = new HashMap<>();
		params.put("startList", startList);
	    params.put("endList", endList);
	    params.put("sidoCode", sidoCode);
		return session.selectList(namespace+"selectAllPopular",params);
	
	}
	// 상세페이지 해당 내용 
	public SightDTO getSelectOne(String contentId) {
		return session.selectOne(namespace+"selectOne",contentId);
	}
}
