class SurfaceCalibration:
    def __init__(self):
        self.is_calibrated = False
        self.calibration_points = []
        self.calibration_complete_callback = None
    
    def start_calibration(self, callback=None):
        """Start the calibration process"""
        self.is_calibrated = False
        self.calibration_points = []
        self.calibration_complete_callback = callback
        print("Калибровка начата")
    
    def add_calibration_point(self, point):
        """Add a calibration point (x, y)"""
        if len(self.calibration_points) < 4:  # Собираем 4 точки для простой калибровки
            self.calibration_points.append(point)
            print(f"Добавлена точка калибровки {len(self.calibration_points)}: {point}")
            
            if len(self.calibration_points) == 4:
                self.complete_calibration()
    
    def complete_calibration(self):
        """Complete the calibration process"""
        self.is_calibrated = True
        print("Калибровка завершена!")
        if self.calibration_complete_callback:
            self.calibration_complete_callback(self.calibration_points)
    
    def get_calibration_status(self):
        """Return current calibration status"""
        return {
            "is_calibrated": self.is_calibrated,
            "points_collected": len(self.calibration_points),
            "points_needed": 4
        }