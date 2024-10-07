package com.acorn.tour.hotkok;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.stereotype.Repository;


import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class HotkokRepository {

	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.HotkokMapper.";
    
    public List<HotkokDTO> getTravelInfo(int sidocode, int index) {
    	int start = (index - 1) * 12 + 1;
        int end = index * 12;
        Map<String, Object> params = new HashMap<>();
		params.put("sidocode", sidocode);
	    params.put("start", start);
	    params.put("end", end);
        return session.selectList(namespace+"getTravelInfo",params);
    }

    public List<HotkokDTO> getFoodInfo(int sidocode, int index) {
    	int start = (index - 1) * 12 + 1;
        int end = index * 12;
        Map<String, Object> params = new HashMap<>();
		params.put("sidocode", sidocode);
	    params.put("start", start);
	    params.put("end", end);
        return session.selectList(namespace+"getFoodInfo",params);
    }
}