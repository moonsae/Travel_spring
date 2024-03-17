package com.acorn.tour.mycourse;

import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.acorn.tour.paging.PageHandler;

@Component
public class MycourseRepository {
	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.MycourseMapper.";
	// 나의 코스 목록 조회
	public List<MycourseDTO> getSelectMyCourse(String userId){
		return session.selectList(namespace+"selectMyCourse",userId);
	}
	// 나의 코스 목록 삽입
	public void getInsertMyCourse(String userId, String courseName) {
		Map<String, Object> params = new HashMap<>();
		params.put("userId", userId);
	    params.put("courseName", courseName);
	    session.insert(namespace+"insertMyCourse",params);
	}
	// 나의 코스 목록 삭제
	public void getDeleteMyCourse(String userId, String coursecode) {
		Map<String, Object> params = new HashMap<>();
		params.put("userId", userId);
	    params.put("coursecode", coursecode);
	    session.delete(namespace+"deleteMyCourse",params);
	}
	
	// 나의코스상세내용 조회 
	public MycourseDTO getSelectOneMyCourse(String userid, String coursecode) {
		Map<String, Object> params = new HashMap<>();
		params.put("userId", userid);
	    params.put("coursecode", coursecode);
	    return session.selectOne(namespace+"selectOneMyCourse",params);
	}
	
	// 나의코스상세내용 수정
	public void getUpdateMyCourse(MycourseDTO item) {
		session.update(namespace+"updateMyCourse",item);
	}
	
	// 나의 코스 상세리스트 조회
	public List<MycourseDTO> getSelectMycourseList(String coursecode) {
		return session.selectList(namespace+"selectMycourseList",coursecode);
	}
	
	
	
	//나의 코스 상세리스트 삽입여부 판단
	public Integer getCountInsertMycourseList(String coursecode, String contentid) {
		Map<String, Object> params = new HashMap<>();
		params.put("coursecode", coursecode);
	    params.put("contentid", contentid);
		int result = session.selectOne(namespace+"countInsertMycourseList",params);
		return result;
	}
	
	// 나의 코스 상세리스트 삽입
	public void getInsertMyCourseList(String coursecode, String contentid) {
		List<MycourseDTO> list = session.selectList(namespace+"selectMycourseList"+contentid);
		int contentnum = 0;
		if(list.size() != 0 ) {
			contentnum = list.get(list.size()-1).getContentnum();
		}
		//int contentnum = rep.countMycourseList(coursecode);
		Map<String, Object> params = new HashMap<>();
		params.put("coursecode", coursecode);
	    params.put("contentid", contentid);
	    params.put("contentnum", contentnum);
		session.insert(namespace+"insertMyCourseList",params);
	}
	
	//나의 코스 상세리스트 삭제
	public void getDeleteMyCourseList(String coursecode, String contentid) {
		Map<String, Object> params = new HashMap<>();
		params.put("coursecode", coursecode);
	    params.put("contentid", contentid);
	    session.delete(namespace+"deleteMyCourseList",params);
	}
	
	// 페이징
	public PageHandler getPaging(int currentPage, String userId) {
		
		int totRecords = getSelectMyCourse(userId).size();
		if(totRecords == 0 ) {
			totRecords = 1;
		}
		int pageSize = 10; // 한 페이지에 표출할 리스트 수
		int grpSize = 5;
		
		PageHandler handler = new PageHandler(currentPage, totRecords, pageSize, grpSize);
		return handler;
	}
	
}
