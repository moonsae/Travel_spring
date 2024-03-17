package com.acorn.tour.myQA;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import javax.sql.DataSource;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

@Repository
public class MyQARepository {

	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.MyQAMapper.";
	// 나의 문의 전체조회
	public List<MyQADTO> getSelectMyQAList(String userid){
		return session.selectList(namespace+"selectMyQA",userid);
	}
	
	// 나의 문의 조회
	public MyQADTO getSelectOneMyQA(String qacode){
		return session.selectOne(namespace+"selectOneMyQA",qacode);
	}
	
	// 나의 문의 등록
	public void getInsertMyQA(MyQADTO item ) {
		session.insert(namespace+"insertMyQA",item);
	}
	
	// 나의 문의 수정
	public void getUpdateMyQA(MyQADTO item ) {
		session.update(namespace+"updateMyQA",item);
	}
	
	// 나의질문 삭제
	public void getDeleteMyQA(String qacode) {
		session.delete(namespace+"deleteMyQA",qacode);
	}

	
		
}
