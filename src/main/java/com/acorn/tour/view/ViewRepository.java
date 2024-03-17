package com.acorn.tour.view;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;



@Component
public class ViewRepository {

	
	@Autowired
	private SqlSession sqlsession;
	
	private static String namespace = "com.acorn.tour.ContentMapper.";
	
	// 조회수 증가
	public void updateContentView(String contentid) {
		sqlsession.update(namespace + "updateContentView", contentid);
	}
	
	
}
