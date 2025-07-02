package com.huy.husci.repository;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.huy.husci.repository.entity.Announcement;

public interface AnnouncementRepository extends MongoRepository<Announcement, String> {
}
