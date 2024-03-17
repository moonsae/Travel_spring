package com.acorn.tour.myreview;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.acorn.tour.login.LoginRepository;
import com.acorn.tour.paging.PageHandler;
import com.acorn.tour.user.UserDTO;


@Controller
public class MyReviewController {
	
	
	@Autowired
	LoginRepository logs;
	
	@Autowired
	MyReviewService mrs;
	
	@Autowired
	MyReviewRepository mrr;
	
	@Autowired
	HttpSession session;
	
	@ResponseBody
	@RequestMapping(value="/mypagereviewlist" , method=RequestMethod.GET)
    public Map<String, Object> mypagereviewList(@RequestParam(required=true) int currentPage,int parentcode) {
		String userId = (String)session.getAttribute("userId");
		Map<String, Object> map  = new HashMap<>();
		
		
		ArrayList<MyReviewDTO> list = mrs.getSelectMyreview(userId, parentcode);
		map.put("reviewlist", list);
		
		UserDTO user = logs.getUser(userId);
		map.put("user", user);
		
		PageHandler handler = mrs.getPaging(currentPage, userId, parentcode);
		map.put("handler" , handler);
		
		
		
        return map;
    }
	
	@ResponseBody
	@RequestMapping(value="/deletemyreview" , method=RequestMethod.POST)
    public void deleteMyReview(@RequestParam(required=true) int reviewcode) {
		mrr.getDeletereviews(reviewcode);
    }

}
