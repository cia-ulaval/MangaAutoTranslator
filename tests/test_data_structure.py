from manga_auto_translator.data_structure import BubbleData

class TestBubbleDataClass:
    bubble_data = BubbleData(
        original_img=[[0, 1], [2, 3]],
        coordinates=[0, 1, 2, 3],
        infered_text='test english',
        translated_text='test francais',
        translated_img=[[4, 5], [6, 7]]
    )
    
    def test_should_verify_all_attributes_are_instancied_when_class_instancied(self) -> None:
        assert hasattr(self.bubble_data, 'original_img'), 'original_img attribute missing'
        assert hasattr(self.bubble_data, 'coordinates'), 'coordinates attribute missing'
        assert hasattr(self.bubble_data, 'infered_text'), 'infered_text attribute missing'
        assert hasattr(self.bubble_data, 'translated_text'), 'translated_text attribute missing'
        assert hasattr(self.bubble_data, 'translated_img'), 'translated_img attribute missing'
        assert hasattr(self.bubble_data, 'id'), 'id attribute missing'
    
    def test_should_verify_width_and_height_values_when_requested(self) -> None:
        assert self.bubble_data.width == 2
        assert self.bubble_data.height == 2
    
    def test_should_check_id_value_when_multiple_classes_are_instancied(self) -> None:
        bubble_data_1 = BubbleData([[0, 0], [0, 0]], [0, 0, 0, 0])
        bubble_data_2 = BubbleData([[0, 0], [0, 0]], [0, 0, 0, 0])
        
        assert self.bubble_data.id == 0
        assert bubble_data_1.id == 1
        assert bubble_data_2.id == 2