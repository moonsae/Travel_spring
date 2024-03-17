package com.acorn.tour.map;

import java.util.HashMap;
import java.util.List;
import java.util.Map;


import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.acorn.tour.hotkok.HotkokDTO;

@Repository
public class MapRepository {

	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.MapMapper.";
	
	public List<MapDTO> getAllMapInfo() {
        return session.selectList(namespace+"getAllMapInfo");
    }
	
	public List<MapDTO> getAllMapInfoByCategory(String category) {
	    return session.selectList(namespace+"getAllMapInfoByCategory",category);
	}
	
	// 주변 여행지 조회
	public List<MapDTO> getAllMapInfo(String title, String firstimage){
		Map<String, Object> params = new HashMap<>();
		params.put("title", title);
	    params.put("firstimage", firstimage);
	    return session.selectList(namespace+"getMapInfoByTitleAndImage",params);
	}

	
}