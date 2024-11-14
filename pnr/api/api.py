# Scrapping API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.utils import get_model
from utils.scrapping_utils import PnrScrapping
from django_extensions.db.models import ActivatorModel
from pnr.api.serializer import PnrDetailSerializer, PnrSerializer
from utils.exceptions import PNRNotFound
from pnr.tasks import send_pnr_details, multiple_pnr_found
from pnr.constants import ReponseMessages
from django.utils.timezone import now

PnrDetail = get_model(app_name="pnr", model_name="PnrDetail")
PassengerDetail = get_model(app_name="pnr", model_name="PassengerDetail")


class PnrScrapper(APIView):
    """PNR Scrapping API"""

    def get(self, request):
        """Get Request to Mail PNR Details"""
        # Validate PNR Number.
        pnr_serializer = PnrSerializer(data=request.query_params)
        pnr_serializer.is_valid(raise_exception=True)
        try:
            # Check if PNR details are available in Database.
            pnr_details = PnrDetail.objects.prefetch_related("passengers_details").get(
                pnr=pnr_serializer.validated_data["pnr"],
                expiry__gt=now(),
            )
            if pnr_details.status == ActivatorModel.INACTIVE_STATUS:
                return Response(
                    {"message": ReponseMessages.FLUSHED_PNR},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = PnrDetailSerializer(pnr_details)
            # Mail PNR Details to User.
            send_pnr_details.delay(request.user.id, serializer.data["id"])
            return Response(
                {"message": ReponseMessages.PNR_DETAILS_MAILED},
                status=status.HTTP_200_OK,
            )
        except PnrDetail.DoesNotExist:
            # Else, Send error 404, PNR not available in Database.
            return Response(
                {"message": ReponseMessages.PNR_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as err:
            # Handle Others Exceptions with Status code 500
            return Response(
                {"message": [str(err)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        pnr_serializer = PnrSerializer(data=request.data)
        pnr_serializer.is_valid(raise_exception=True)
        try:
            # If PNR Exists in database return data from database
            pnr_details = PnrDetail.objects.prefetch_related("passengers_details").get(
                pnr=pnr_serializer.validated_data["pnr"],
                expiry__gt=now(),
            )
            if pnr_details.status == ActivatorModel.INACTIVE_STATUS:
                return Response(
                    {"message": ReponseMessages.FLUSHED_PNR},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = PnrDetailSerializer(pnr_details)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PnrDetail.DoesNotExist:
            # If PNR Not Exists Fetch PNR.
            try:
                scrapper = PnrScrapping(pnr_serializer.validated_data["pnr"])
                data = scrapper()
                data["users"] = [request.user.id]
                serializer = PnrDetailSerializer(data=data)
                serializer.is_valid(raise_exception=True)

                # Check if PNR Details Already Exist Once Again to handle same pnr number checked simuntaneously.
                try:
                    PnrDetail.objects.get(
                        pnr=pnr_serializer.validated_data["pnr"],
                        status=ActivatorModel.ACTIVE_STATUS,
                    )
                except PnrDetail.DoesNotExist:
                    # If PNR details not available create details.
                    serializer.save()
                    send_pnr_details.delay(
                        request.user.id, serializer.data["id"]
                    )  # TODO: Use Signals to Send Pnr Details
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except PNRNotFound as pnr_not_found:
                # Handle others exception related to Scrapping PNR.
                return Response(
                    {"message": [str(pnr_not_found)]}, status=status.HTTP_404_NOT_FOUND
                )
        except PnrDetail.MultipleObjectsReturned:
            # If Multiple PNR found Delete PNR details while exclude last modified PNR.
            multiple_pnr_found.delay(pnr_serializer.validated_data["pnr"])
            return Response(
                {"message": [ReponseMessages.MULTIPLE_PNR_FOUND]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            # Handle others exception related to PNR.
            return Response(
                {"message": [str(err)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        # Validate PNR number.
        pnr_serializer = PnrSerializer(data=request.data)
        pnr_serializer.is_valid(raise_exception=True)
        try:
            # Get the PNR object from Model.
            obj = PnrDetail.objects.prefetch_related("passengers_details").get(
                pnr=pnr_serializer.validated_data["pnr"],
                expiry__gt=now(),
            )
            if obj.status == ActivatorModel.INACTIVE_STATUS:
                return Response(
                    {"message": ReponseMessages.FLUSHED_PNR},
                    status=status.HTTP_404_NOT_FOUND,
                )
            # Scrap Updated Details
            scrapper = PnrScrapping(pnr_serializer.validated_data["pnr"])
            data = scrapper()
            # Update PNR Details.
            serializer = PnrDetailSerializer(obj, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Mail Updated Details.
            send_pnr_details.delay(request.user.id, serializer.data["id"])
            # Return Updated Details.
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PnrDetail.DoesNotExist:
            # PNR Details Not Available to Update Please Fetch First.
            return Response(
                {"message": [ReponseMessages.PNR_NOT_FOUND]},
                status=status.HTTP_404_NOT_FOUND,
            )
        except PnrDetail.MultipleObjectsReturned:
            # PNR Details Multiple Objects Retured, Also Handles Multiple PNR Details, Only Excluse Last Modified PNR, Else Delete *.
            multiple_pnr_found.delay(pnr_serializer.validated_data["pnr"])
            return Response(
                {"message": [ReponseMessages.MULTIPLE_PNR_FOUND]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # Handle Others Exceptions with Status code 500
            return Response(
                {"message": [str(e)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
