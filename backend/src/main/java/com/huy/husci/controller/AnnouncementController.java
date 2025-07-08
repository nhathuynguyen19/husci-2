package com.huy.husci.controller;

import com.huy.husci.repository.entity.Announcement;
import com.huy.husci.repository.entity.Student;
import com.huy.husci.response.ApiResponse;
import com.huy.husci.service.AnnouncementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.web.bind.annotation.*;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/announcements")
public class AnnouncementController {
    @Autowired
    private final AnnouncementService announcementService;

    public AnnouncementController(AnnouncementService announcementService) {
        this.announcementService = announcementService;
    }

    // get all
    @GetMapping
    public ApiResponse getAllAnnouncements() {
        List<Announcement> announcements = announcementService.getAllAnnouncements();
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        returnData.put("announcements", announcements);
        return ApiResponse.success(returnData);
    }

    // add
//    @PostMapping
//    public ApiResponse addAnnouncement(@RequestBody Announcement announcement) {
//        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
//        announcement.setId(announcement.getId().toLowerCase());
//        returnData.put("announcement", announcementService.addAnnouncement(announcement));
//        return ApiResponse.success(returnData);
//    }

    // update by id
//    @PutMapping("/{id}")
//    public ApiResponse updateAnnouncement(@PathVariable String id,@RequestBody Announcement announcement) {
//        announcement = announcementService.updateAnnouncement(id.toLowerCase(), announcement);
//        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
//        returnData.put("announcement", announcement);
//        return ApiResponse.success(returnData);
//    }

    // delete by id
//    @DeleteMapping("/{id}")
//    public ApiResponse deleteAnnouncement(@PathVariable String id) {
//        announcementService.deleteAnnouncement(id.toLowerCase());
//        return ApiResponse.success();
//    }

    // get by id
    @GetMapping("/{id}")
    public ApiResponse getAnnouncementById(@PathVariable String id) {
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        Announcement announcement = announcementService.getAnnouncementById(id.toLowerCase());
        if (announcement != null) {
            returnData.put("announcement", announcement);
            return ApiResponse.success(returnData);
        } else {
            return ApiResponse.failMessage("Not Found Id Announcement: " + id.toLowerCase());
        }
    }
}
