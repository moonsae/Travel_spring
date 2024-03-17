package com.acorn.tour.myreview;

import java.sql.Connection;
import java.sql.Date;
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



@Component
public class MyReviewRepository {
	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.MyReviewMapper.";
	
	// 해당게시물 나의 리뷰 목록 전체 조회

	public List<MyReviewDTO> getSelectMyreviewList(String userid, int parentcode) {
		Map<String, Object> params = new HashMap<>();
		params.put("userid", userid);
	    params.put("parentcode", parentcode);
	    return session.selectList(namespace+"selectMyReview",params);
	}
	
	// 해당 게시물 리뷰 삭제
	public void getDeletereviews(int reviewcode) {
		session.delete(namespace+"deleteReviews",reviewcode);
	}
		

}
