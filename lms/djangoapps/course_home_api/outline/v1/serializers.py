"""
Outline Tab Serializers.
"""


from rest_framework import serializers
from lms.djangoapps.courseware.date_summary import VerificationDeadlineDate

#TODO: @dlichen take all the information and make sure it's ready to send to the MFE
class CourseToolSerializer(serializers.Serializer):
    """
    Serializer for Course Tool Objects
    """
    analytics_id = serializers.CharField()
    title = serializers.CharField()
    url = serializers.SerializerMethodField()
    #TODO: @dlichen you may want to manipulate the data before sending it back to the MFE

    def get_url(self, tool):
        course_key = self.context.get('course_key')
        #TODO: @dlichen - note 18000 is course home and localhost:20000 points to the MFE
        url = tool.url(course_key)
        request = self.context.get('request')
        return request.build_absolute_uri(url)


class DateSummarySerializer(serializers.Serializer):
    """
    Serializer for Date Summary Objects.
    """
    date = serializers.DateTimeField()
    date_type = serializers.CharField()
    description = serializers.CharField()
    learner_has_access = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    title = serializers.CharField()
    link_text = serializers.CharField()
    title_html = serializers.CharField()

    def get_learner_has_access(self, block):
        learner_is_full_access = self.context.get('learner_is_full_access', False)
        block_is_verified = (getattr(block, 'contains_gated_content', False) or
                             isinstance(block, VerificationDeadlineDate))
        return (not block_is_verified) or learner_is_full_access

    def get_link(self, block):
        if block.link:
            request = self.context.get('request')
            return request.build_absolute_uri(block.link)
        return ''


class OutlineTabSerializer(serializers.Serializer):
    """
    Serializer for the Outline Tab
    """
    course_tools = CourseToolSerializer(many=True)
    course_date_blocks = DateSummarySerializer(many=True)
    user_timezone = serializers.CharField()
    #TODO: @dlichen write a serializer with many=True, which understands that there's a list and loops through it
