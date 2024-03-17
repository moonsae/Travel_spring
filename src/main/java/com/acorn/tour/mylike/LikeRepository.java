package com.acorn.tour.mylike;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.sql.DataSource;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

import com.acorn.tour.mycourse.MycourseDTO;



@Repository
public class LikeRepository {
	
	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.MyLikeMapper.";
	
	// 좋아요 삽입
	public void getUpdateContentLike(String contentId, String userId) {
		Map<String, Object> params = new HashMap<>();
		params.put("userId", userId);
	    params.put("contentId", contentId);
		session.insert(namespace+"updateContentLike",params);
	}
	// 좋아요 삭제
	public void getDeleteContentLike(String contentId, String userId) {
		Map<String, Object> params = new HashMap<>();
		params.put("userId", userId);
	    params.put("contentId", contentId);
	    session.delete(namespace+"deleteContentLike",params);
	}
	
	// 좋아요 수 조회
	public Integer getCountLike(String contentId) {
		int result = session.selectOne(namespace+"countLike",contentId);
		return result;
	}
	
	// 나의 좋아요 수 조회
	public Integer getMycountLike(String contentId, String userId) {
		Map<String, Object> params = new HashMap<>();
		params.put("userId", userId);
	    params.put("contentId", contentId);
		int result = session.selectOne(namespace+"mycountLike",params);
		return result;
	}
	
	// 좋아요 목록 조회
	public List<LikeDTO> getmyLikeList(String userId){
		return session.selectList(namespace+"myLike",userId);
	}
}
