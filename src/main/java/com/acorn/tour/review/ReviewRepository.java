package com.acorn.tour.review;

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



@Component
public class ReviewRepository {
	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.ReviewMapper.";
	// 해당 게시물 리뷰 전체 조회
	public List<ReviewDTO> getReview(String contentid) {
		return session.selectList(namespace+"selectReviewsByContentId",contentid);
	}
	
	// 해당 게시물 리뷰 등록
	public void insertReview(String userid, String contentid, String content) {
	    Map<String, Object> params = new HashMap<>();
	    params.put("userid", userid);
	    params.put("content", content);
	    params.put("contentid", contentid);
	    session.insert(namespace + "insertReview", params);
	}
	
	// 해당 게시물 리뷰 수정
	public void getUpdatereviews(int reviewcode, String content) {
		Map<String, Object> params = new HashMap<>();
		params.put("reviewcode", reviewcode);
	    params.put("content", content);
	    session.update(namespace+"updateReview",params);
	}
	
	// 해당 게시물 리뷰 삭제 및 답글 삭제
	public void getDeletereviews(int reviewcode) {
		session.delete(namespace+"deleteReview",reviewcode);
	}
	
	// 답글 조회
	public List<ReviewDTO> selectReply(int parentcode){
		return session.selectList(namespace+"selectReplyByParentCode",parentcode);
	}
	
	// 답글 등록
	public void getInsertReply(ReviewDTO review) {
		session.insert(namespace+"insertReply",review);
	}
	
	// 답글 수정
	public void getUpdateReply(int reviewcode, String content) {
		Map<String, Object> params = new HashMap<>();
		params.put("reviewcode", reviewcode);
	    params.put("content", content);
	    session.update(namespace+"updateReply",params);
	}
	

}
