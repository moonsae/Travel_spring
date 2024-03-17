package com.acorn.tour.sido;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import javax.sql.DataSource;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

@Repository
public class SidoRepository {
	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.SidoMapper.";
	
	// 시도리스트 전체 출력
	public List<SidoDTO> selectAll() {
		return session.selectList(namespace+"selectAllFromSidoTbl");
	
}
}
