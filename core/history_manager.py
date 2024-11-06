from collections import deque
import numpy as np

class HistoryManager:
    def __init__(self):
        self.y_history = {
            'index': deque(maxlen=12),
            'middle': deque(maxlen=12),
            'ring': deque(maxlen=12),
            'pinky': deque(maxlen=12)
        }
        
        self.x_history = {
            'index': deque(maxlen=12),
            'middle': deque(maxlen=12)
        }
        
        self.size_history = deque(maxlen=6)
        self.size_change_history = deque(maxlen=50)
        
        self.finger_tips_history = [deque(maxlen=3) for _ in range(5)]
        
        self.hand_center_history = deque(maxlen=6)
        
        self.threshold_y = 3.5
        self.threshold_size = 0.04
        self.threshold_size_change = 0.008
        
        self._cached_movement = None
        self._last_cache_time = 0
        self._cache_valid_frames = 2
        self._frame_counter = 0
        self._last_size_smooth = None
        
    def update_positions(self, index_tip, middle_tip, ring_tip, pinky_tip, hand_size, hand_center):
        self._frame_counter += 1
        
        self.y_history['index'].append(index_tip[1])
        self.y_history['middle'].append(middle_tip[1])
        self.y_history['ring'].append(ring_tip[1])
        self.y_history['pinky'].append(pinky_tip[1])
        
        self.x_history['index'].append(index_tip[0])
        self.x_history['middle'].append(middle_tip[0])
        
        if self._last_size_smooth is None:
            self._last_size_smooth = hand_size
        else:
            smoothing = 0.7
            hand_size = hand_size * (1 - smoothing) + self._last_size_smooth * smoothing
            self._last_size_smooth = hand_size
        
        self.size_history.append(hand_size)
        self.hand_center_history.append(np.array(hand_center))
        
        if self._frame_counter - self._last_cache_time > self._cache_valid_frames:
            self._cached_movement = None
        
        if len(self.size_history) >= 2:
            size_change = abs(hand_size - list(self.size_history)[-2]) / list(self.size_history)[-2]
            if size_change > self.threshold_size_change:
                self.size_change_history.append(size_change)
    
    def get_size_changes(self):
        if len(self.size_history) < 2:
            return np.array([])
        
        size_array = np.array(list(self.size_history))
        changes = np.diff(size_array) / size_array[:-1]
        return changes
    
    def is_size_stable(self):
        if len(self.size_history) < 2:
            return True
            
        recent_changes = list(self.size_history)[-4:]
        if len(recent_changes) < 2:
            return True
            
        changes = np.diff(recent_changes) / np.array(recent_changes[:-1])
        return np.mean(np.abs(changes)) <= self.threshold_size
    
    def get_movement_amount(self):
        if len(self.hand_center_history) < 2:
            return 0
            
        if (self._cached_movement is not None and 
            self._frame_counter - self._last_cache_time <= self._cache_valid_frames):
            return self._cached_movement
            
        movement = np.linalg.norm(self.hand_center_history[-1] - self.hand_center_history[0])
        
        self._cached_movement = movement
        self._last_cache_time = self._frame_counter
        
        return movement
    
    def update_finger_tips(self, finger_tips):
        for i, tip in enumerate(finger_tips):
            self.finger_tips_history[i].append(np.array(tip))
    
    def get_finger_movement(self, finger_index):
        if len(self.finger_tips_history[finger_index]) < 2:
            return 0
        return np.linalg.norm(
            self.finger_tips_history[finger_index][-1] - 
            self.finger_tips_history[finger_index][0]
        )
    
    def get_average_movement(self):
        movements = [self.get_finger_movement(i) for i in range(5)]
        return np.mean([m for m in movements if m > 0]) if movements else 0
    
    def reset(self):
        for collection in [self.y_history, self.x_history]:
            for deq in collection.values():
                deq.clear()
        
        self.size_history.clear()
        self.size_change_history.clear()
        
        for history in self.finger_tips_history:
            history.clear()
        
        self.hand_center_history.clear()
        
        self._cached_movement = None
        self._last_cache_time = 0
        self._frame_counter = 0
        self._last_size_smooth = None