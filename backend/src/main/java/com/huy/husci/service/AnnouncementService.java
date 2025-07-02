package com.huy.husci.service;

import com.huy.husci.repository.AnnouncementRepository;
import com.huy.husci.repository.entity.Announcement;
import com.huy.husci.utils.event.AnnouncementCreatedEvent;
import com.huy.husci.utils.event.AnnouncementDeletedEvent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class AnnouncementService {
    @Autowired
    private AnnouncementRepository announcementRepository;

    @Autowired
    private ApplicationEventPublisher publisher;

    public boolean isAnnouncement(String id) {
        return this.announcementRepository.findById(id).isPresent();
    }

    public AnnouncementService(AnnouncementRepository announcementRepository) {
        this.announcementRepository = announcementRepository;
    }

    public Announcement addAnnouncement(Announcement announcement) {
        if (!isAnnouncement(announcement.getId())) {
            Announcement saved = announcementRepository.save(announcement);
//            publisher.publishEvent(new AnnouncementCreatedEvent(saved));
            return saved;
        }
        return null;
    }

    public Announcement getAnnouncementById(String id) {
        return announcementRepository.findById(id).orElse(null);
    }

    public Announcement updateAnnouncement(String id, Announcement announcement) {
        Optional<Announcement> optionalAnnouncement = announcementRepository.findById(id);
        if (optionalAnnouncement.isPresent()) {
            Announcement existingAnnouncement = optionalAnnouncement.get();
            existingAnnouncement.setTitle(announcement.getTitle());
            existingAnnouncement.setContent(announcement.getContent());
            existingAnnouncement.setUrl(announcement.getUrl());
            existingAnnouncement.setDateCreate(announcement.getDateCreate());
            return announcementRepository.save(existingAnnouncement);
        } else {
            throw new IllegalArgumentException("Announcement with id: " + id + " not found!");
        }
    }

    public void deleteAnnouncement(String id) {
        Optional<Announcement> announcement = announcementRepository.findById(id);
        if (announcement.isPresent()) {
            Announcement deleted = announcement.get();
            announcementRepository.deleteById(id);
//            publisher.publishEvent(new AnnouncementDeletedEvent(deleted));
        }
    }

    public List<Announcement> getAllAnnouncements() {
        return announcementRepository.findAll();
    }
}
