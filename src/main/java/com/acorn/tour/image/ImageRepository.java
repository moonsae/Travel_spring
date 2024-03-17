package com.acorn.tour.image;

import java.util.List;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;



@Component
public class ImageRepository {
	
	@Autowired
	private SqlSession session;
	
	private static String namespace = "com.acorn.tour.ContentMapper.";
	
	
	// 상세페이지 이미지
	public List<ImageDTO> selectImg(String contentId) {
		return session.selectList(namespace+"selectImg",contentId);
	}
	
}
