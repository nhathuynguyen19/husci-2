package com.huy.husci.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.huy.husci.repository.entity.Announcement;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface AnnouncementRepository extends MongoRepository<Announcement, Long> {
}
