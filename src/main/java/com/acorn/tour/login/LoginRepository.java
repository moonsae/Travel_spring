package com.acorn.tour.login;

import java.util.HashMap;
import java.util.Map;


import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.acorn.tour.user.UserDTO;

@Repository
public class LoginRepository {
	
	@Autowired
	private SqlSession session;
	private static String namespace = "com.acorn.LoginMapper.";
	
	public boolean isValidUser(String userid, String pw) {
		Map<String, Object> params = new HashMap<>();
		params.put("id", userid);
	    params.put("pw", pw);
	    
	    int count = session.selectOne(namespace + "isValid", params);
	    return count > 0;
    }
	 
	public UserDTO getUser(String id) {
		return session.selectOne(namespace+"getUser",id);
	}
	
	public int registerKakao(String user_kakao, String nickname, String profile_image) {
		Map<String, Object> params = new HashMap<>();
	    params.put("user_kakao", user_kakao);
	    params.put("nickname", nickname);
	    params.put("profile_image", profile_image);
	    return session.insert(namespace+"register",params);
	}
 
	public boolean isMember(String user_kakao) {		 
		int count = session.selectOne(namespace+"isMember",user_kakao);
		return count>0;
	}
	
	
}