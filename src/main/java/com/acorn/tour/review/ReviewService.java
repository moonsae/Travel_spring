package com.acorn.tour.review;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;



@Component
public class ReviewService {
	
	
	@Autowired
	ReviewRepository rep;
	
	// 해당 게시물 리뷰 전체 조회
	public ArrayList<ReviewDTO> getList(String contentid) {
		ArrayList<ReviewDTO> list = (ArrayList<ReviewDTO>) rep.getReview(contentid);
		return list;
	}
	// 해당 게시물 리뷰 등록
	public void getInsertreviews(String userid, String contentid, String content) {
		rep.insertReview(userid, contentid, content);
	}
	// 해당 게시물 리뷰 수정
	public void getUpdatereviews(int reviewcode, String content) {
		rep.getUpdatereviews(reviewcode, content);
	}
	// 해당 게시물 리뷰 삭제 및 답글 삭제
	public void getDeletereviews(int reviewcode) {
		rep.getDeletereviews(reviewcode);
	}
	// 답글 조회
	public ArrayList<ReviewDTO> getSelectReply(int parentcode){
		ArrayList<ReviewDTO> list = (ArrayList<ReviewDTO>) rep.selectReply(parentcode);
		return list;
	}
	// 답글 등록
	public void getInsertReply(ReviewDTO review) {
		rep.getInsertReply(review);
	}
	
	// 답글 수정
	public void getUpdateReply(int reviewcode, String content) {
		rep.getUpdateReply(reviewcode, content);
	}

	
	
	

}
