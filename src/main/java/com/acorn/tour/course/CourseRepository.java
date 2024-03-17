package com.acorn.tour.course;


import java.util.HashMap;
import java.util.List;
import java.util.Map;


import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;



@Component
public class CourseRepository {

	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.CourseMapper.";
	
	// content 전체 갯수
	public Integer totalCnt(int sidoCode) {
		int result = session.selectOne(namespace+"totalCnt",sidoCode);
		return result;
	}
	
	// 지역별 최신순 content 10개씩 조회
	public List<CourseDTO> selectAllLatest(int startList, int endList, int sidoCode) {
		Map<String, Object> params = new HashMap<>();
		params.put("startList", startList);
	    params.put("endList", endList);
	    params.put("sidoCode", sidoCode);
		return session.selectList(namespace+"selectAllLatest",params);
	}
		
	
	// 인기순 
	public List<CourseDTO> selectAllPopular(int startList, int endList, int sidoCode) {
		Map<String, Object> params = new HashMap<>();
		params.put("startList", startList);
	    params.put("endList", endList);
	    params.put("sidoCode", sidoCode);
		return session.selectList(namespace+"selectAllPopular",params);
	}
	
	// 상세페이지에 표출할 내용
	public CourseDTO selectOne(String contentId) {
		return session.selectOne(namespace+"selectOne",contentId);
	}
	
	// 상세페이지에 표출할 코스 목록 내용
	public List<CourseContentDTO> selectCourse(String contentId) {
		return session.selectList(namespace+"selectCourse",contentId);
		
	}
	
}
